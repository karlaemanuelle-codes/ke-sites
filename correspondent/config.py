"""Carregamento e validação da configuração do correspondente."""

import json
from pathlib import Path

PUBLIC_COMPLIANCE_GROUPS = (
    "certificacoes",
    "credenciamentos",
    "instituicoesParceiras",
    "bancos",
    "informacoesRegulatorias",
    "dadosEmpresa",
    "dadosProfissionais",
)


def load_config(path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_config(config)
    return config


def validate_config(config):
    compliance = config.get("compliance", {})
    if not compliance.get("textoInstitucionalSeguro"):
        raise ValueError("O texto institucional seguro é obrigatório.")

    for group in PUBLIC_COMPLIANCE_GROUPS:
        items = compliance.get(group, [])
        if not isinstance(items, list):
            raise ValueError(f"{group} deve ser uma lista.")
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"Cada item de {group} deve ser um objeto.")
            if item.get("publicar") and not item.get("confirmado"):
                raise ValueError(f"Item não confirmado não pode ser publicado em {group}.")
            if item.get("publicar") and not item.get("texto"):
                raise ValueError(f"Item público sem texto em {group}.")

    review = config.get("avaliacoes", {})
    if review.get("exigirAutorizacaoPublicacao") is not True:
        raise ValueError("A autorização para publicar avaliações deve ser obrigatória.")
    if review.get("exigirAprovacaoManual") is not True:
        raise ValueError("A aprovação manual de avaliações deve ser obrigatória.")


def public_compliance(config):
    compliance = config["compliance"]
    result = {"textoInstitucional": compliance["textoInstitucionalSeguro"]}
    for group in PUBLIC_COMPLIANCE_GROUPS:
        result[group] = [
            {"texto": item["texto"]}
            for item in compliance.get(group, [])
            if item.get("confirmado") and item.get("publicar") and item.get("texto")
        ]
    return result
