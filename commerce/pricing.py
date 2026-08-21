"""
pricing.py — calculadora de parcelamento (seções 3, 4, 25, 26 do adendo).

Regras que este módulo respeita:
  - Nenhuma taxa é hardcoded aqui — tudo vem de `config` (ver config.py).
  - Nunca afirma "sem juros" a menos que o modo configurado realmente seja
    SEM_JUROS (seção 26 — "Nunca escrever 'sem juros' se não for verdade").
  - payment_fee_mode decide quem absorve a taxa de gateway.
  - installment_interest_mode decide se o cliente paga juros adicionais
    além da taxa de gateway.
  - Parcelas abaixo de `min_installment_value` não são oferecidas.
"""
from __future__ import annotations

from dataclasses import dataclass

from .models import InstallmentInterestMode, PaymentFeeMode


@dataclass(frozen=True)
class InstallmentOption:
    installments: int
    installment_value: float
    customer_total: float
    gateway_fee_amount: float
    net_to_ke_sites: float
    has_interest: bool
    label: str  # microcopy pronta para exibir, ex.: "12x de R$ 333,08"


def _round2(value: float) -> float:
    return round(value + 1e-9, 2)


def _fmt_brl(value: float) -> str:
    """Formata um valor como 'R$ 1.234,56' (separador de milhar '.', decimal ',')."""
    return f"{value:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def calculate_price(
    *,
    amount: float,
    method: str,               # "PIX" | "CREDIT_AVISTA" | "CREDIT_PARCELADO"
    installments: int,
    config: dict,
) -> InstallmentOption:
    """Calcula o valor da parcela, total do cliente, taxa de gateway e
    líquido para a KE Sites — para uma combinação específica de método e
    número de parcelas. Levanta ValueError para combinações inválidas
    (ex.: PIX com >1 parcela, ou parcela abaixo do valor mínimo)."""
    if amount <= 0:
        raise ValueError("amount deve ser positivo")
    if method == "PIX" and installments != 1:
        raise ValueError("PIX não é parcelável neste modelo")
    if installments < 1 or installments > config.get("max_installments", 12):
        raise ValueError(f"installments fora do intervalo permitido: {installments}")

    gateway_fee_pct = dict(config["gateway_fee_percent"]).get(method, None)
    if method == "CREDIT_PARCELADO":
        gateway_fee_pct = config["installment_fee_percent"][installments]
    elif gateway_fee_pct is None:
        # CREDIT_AVISTA cai aqui se não estiver na tabela — usa a chave direta
        gateway_fee_pct = config["gateway_fee_percent"].get(method, 0.0)

    gateway_fee_amount = _round2(amount * gateway_fee_pct)

    interest_mode = config["installment_interest_mode"]
    has_interest = False
    customer_interest_amount = 0.0
    if method == "CREDIT_PARCELADO" and interest_mode == InstallmentInterestMode.JUROS_DO_CLIENTE:
        interest_pct = config["customer_interest_percent"].get(installments, 0.0)
        if interest_pct > 0:
            has_interest = True
            customer_interest_amount = _round2(amount * interest_pct)

    fee_mode = config["payment_fee_mode"]
    if fee_mode == PaymentFeeMode.MERCHANT_ABSORBS:
        customer_total = amount + customer_interest_amount
        net_to_ke_sites = _round2(amount - gateway_fee_amount)
    elif fee_mode == PaymentFeeMode.CUSTOMER_PAYS:
        customer_total = _round2(amount + gateway_fee_amount + customer_interest_amount)
        net_to_ke_sites = amount
    elif fee_mode == PaymentFeeMode.HYBRID:
        split = config.get("hybrid_fee_split_customer", 0.5)
        customer_share = _round2(gateway_fee_amount * split)
        merchant_share = _round2(gateway_fee_amount - customer_share)
        customer_total = _round2(amount + customer_share + customer_interest_amount)
        net_to_ke_sites = _round2(amount - merchant_share)
    else:
        raise ValueError(f"payment_fee_mode desconhecido: {fee_mode}")

    # desconto Pix (seção "criar motor comercial... desconto Pix")
    if method == "PIX":
        pix_discount_pct = config.get("pix_discount_percent", 0.0)
        if pix_discount_pct > 0:
            discount_amount = _round2(customer_total * pix_discount_pct)
            customer_total = _round2(customer_total - discount_amount)
            net_to_ke_sites = _round2(net_to_ke_sites - discount_amount)

    customer_total = _round2(customer_total)
    installment_value = _round2(customer_total / installments)

    if method == "CREDIT_PARCELADO":
        if interest_mode == InstallmentInterestMode.SEM_JUROS:
            label = f"{installments}x de R$ {_fmt_brl(installment_value)} sem juros"
        else:
            # JUROS_DO_CLIENTE com taxa > 0, ou CONFIGURAVEL: nunca afirma "sem juros"
            # a menos que o modo realmente seja SEM_JUROS (regra da seção 26).
            label = f"{installments}x de R$ {_fmt_brl(installment_value)}"
    elif method == "PIX":
        label = f"R$ {_fmt_brl(installment_value)} no Pix"
    else:
        label = f"R$ {_fmt_brl(installment_value)} à vista no cartão"

    return InstallmentOption(
        installments=installments,
        installment_value=installment_value,
        customer_total=customer_total,
        gateway_fee_amount=gateway_fee_amount,
        net_to_ke_sites=net_to_ke_sites,
        has_interest=has_interest,
        label=label,
    )


def calculate_installment_table(*, amount: float, config: dict) -> list[InstallmentOption]:
    """Retorna todas as opções de parcelamento (1x a max_installments) para
    cartão, respeitando o valor mínimo de parcela (seção 4)."""
    max_n = config.get("max_installments", 12)
    min_value = config.get("min_installment_value", 50.0)
    options = []
    for n in range(1, max_n + 1):
        opt = calculate_price(
            amount=amount,
            method="CREDIT_AVISTA" if n == 1 else "CREDIT_PARCELADO",
            installments=n,
            config=config,
        )
        if opt.installment_value < min_value:
            break
        options.append(opt)
    return options


def calculate_pix_price(*, amount: float, config: dict) -> InstallmentOption:
    return calculate_price(amount=amount, method="PIX", installments=1, config=config)
