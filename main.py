import os
import json
import argparse
from extractor import extract_with_fallback, cache


def process_dataset(dataset_path):
    """
    Processa um dataset JSON no formato:
    [
      {
        "label": "RG",
        "extraction_schema": {...},
        "pdf_path": "caminho/para/documento.pdf"
      },
      ...
    ]
    """
    if not os.path.exists(dataset_path):
        print(f"Arquivo não encontrado: {dataset_path}")
        return

    # Abre o arquivo do dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    if not isinstance(dataset, list):
        print("O arquivo dataset precisa conter uma lista de objetos JSON.")
        return

    for i, item in enumerate(dataset, start=1):
        label = item.get("label")
        extraction_schema = item.get("extraction_schema")
        pdf_path = item.get("pdf_path")

        if not all([label, extraction_schema, pdf_path]):
            print(f"Item {i} ignorado — campos obrigatórios ausentes.")
            continue

        if not os.path.exists(pdf_path):
            print(f"PDF não encontrado: {pdf_path}")
            continue

        print(f"\n=== [{i}/{len(dataset)}] Processando '{pdf_path}' (label='{label}') ===")

        results = extract_with_fallback(label, extraction_schema, pdf_path)

        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extrai dados estruturados de PDFs a partir de um dataset JSON."
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Caminho completo para o arquivo dataset.json contendo label, schema e pdf_path."
    )

    args = parser.parse_args()
    process_dataset(args.dataset)
