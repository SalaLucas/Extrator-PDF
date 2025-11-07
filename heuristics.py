import re

def extract_field_with_context(field_name, text, previous_knowledge):
    field_name = field_name.lower()
    text_clean = " ".join(text.split())

    # Tentativa 1 — heurística tradicional
    base_result = _basic_heuristics(field_name, text_clean)
    if base_result["confidence"] >= 0.8:
        return base_result

    # Tentativa 2 — valores anteriores do mesmo label
    for known_field, known_data in previous_knowledge.items():
        if known_data.get("value") and known_data["value"] in text_clean:
            if known_field == field_name:
                return {"value": known_data["value"], "confidence": 0.9}

    # Tentativa 3 — inferência contextual simples
    if "nome" in field_name and "nome_mae" in previous_knowledge:
        match = re.search(r"Nome\s*do\s*Pai[:\s]+([A-ZÀ-Ÿ\s]{3,})", text_clean)
        if match:
            return {"value": match.group(1).title().strip(), "confidence": 0.8}

    return base_result


def _basic_heuristics(field_name, text):
    if field_name in ("cpf", "número de cpf", "cpf do titular"):
        match = re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", text)
        if match:
            return {"value": match.group(), "confidence": 0.9}

    if field_name in ("cnpj", "número de cnpj"):
        match = re.search(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", text)
        if match:
            return {"value": match.group(), "confidence": 0.9}

    if field_name in ("nome", "nome completo", "titular"):
        match = re.search(r"Nome[:\s]+([A-ZÀ-Ÿ\s]{3,})", text)
        if match:
            return {"value": match.group(1).title().strip(), "confidence": 0.8}

    if "data" in field_name:
        match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
        if match:
            return {"value": match.group(), "confidence": 0.8}

    if "valor" in field_name or "total" in field_name:
        match = re.search(r"R?\$ ?\d{1,3}(\.\d{3})*,\d{2}", text)
        if match:
            return {"value": match.group(), "confidence": 0.8}

    if "email" in field_name:
        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if match:
            return {"value": match.group(), "confidence": 0.9}

    return {"value": None, "confidence": 0.0}
