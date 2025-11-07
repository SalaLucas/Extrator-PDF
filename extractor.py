import json
import re
from pdfminer.high_level import extract_text
from heuristics import extract_field_with_context
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-5-mini"
CONFIDENCE_THRESHOLD = 0.75

# Cache apenas para schemas (aprendizado incremental)
cache = {}  # {label: {campo: {"value": str, "confidence": float}}}


def extract_with_fallback(label, extraction_schema, pdf_path):
    if label not in cache:
        cache[label] = {}

    text = extract_text(pdf_path)
    results = {}
    low_conf_fields = {}

    # Primeira fase: heurística
    for field_name, description in extraction_schema.items():
        previous_knowledge = cache[label]
        heur_result = extract_field_with_context(field_name, text, previous_knowledge)
        value = heur_result["value"]
        confidence = heur_result["confidence"]

        results[field_name] = {"value": value, "confidence": confidence}

        # Evita reutilizar o mesmo trecho de texto
        if value and confidence >= 0.7:
            safe_val = str(value).strip()
            if safe_val:
                pattern = re.escape(safe_val)
                text = re.sub(pattern, " " * len(safe_val), text, count=1, flags=re.IGNORECASE)

        if confidence < CONFIDENCE_THRESHOLD:
            low_conf_fields[field_name] = description

    # Segunda fase: GPT para campos de baixa confiança
    if low_conf_fields:
        prompt = build_batch_prompt(low_conf_fields, text)

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Você é um extrator preciso de informações de documentos."},
                    {"role": "user", "content": prompt},
                ],
            )

            gpt_output = response.choices[0].message.content.strip()

            try:
                gpt_data = json_safe_parse(gpt_output)
            except Exception:
                gpt_data = parse_loose_text(gpt_output)

            for field, value in gpt_data.items():
                if field in results:
                    results[field]["value"] = value or None
                    results[field]["confidence"] = 0.95

        except Exception as e:
            print(f"Erro ao chamar GPT: {e}")

    # Atualiza o cache do schema
    for field, data in results.items():
        if data["value"] and data["confidence"] >= 0.8:
            cache[label][field] = data

    # Substitui valores vazios por null e remove confidences antes de retornar
    final_output = {}
    for field, data in results.items():
        final_output[field] = data["value"] if data["value"] else None

    return final_output


def build_batch_prompt(fields_to_extract, text):
    schema_desc = "\n".join([f"- {field}: {desc}" for field, desc in fields_to_extract.items()])
    return f"""
Extraia os seguintes campos do texto abaixo e responda **apenas** com um JSON válido.

Exemplo de formato de saída:
{{
  "campo1": "valor1",
  "campo2": "valor2"
}}

Campos a extrair:
{schema_desc}

Texto:
{text}
"""


def json_safe_parse(content):
    start = content.find("{")
    end = content.rfind("}") + 1
    if start != -1 and end != -1:
        snippet = content[start:end]
        return json.loads(snippet)
    raise ValueError("Nenhum JSON válido encontrado.")


def parse_loose_text(text):
    pairs = re.findall(r"([\w_]+)\s*[:=]\s*([^\n]+)", text)
    return {k.strip(): v.strip() for k, v in pairs}
