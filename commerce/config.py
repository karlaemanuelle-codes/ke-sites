"""
config.py — configuração administrável do motor comercial.

Regra de ouro (seção 4 e 31 do adendo): NENHUMA taxa de gateway é
hardcoded como se fosse definitiva. Tudo aqui é um valor de PARTIDA,
explicitamente marcado como ilustrativo, para que a calculadora funcione
em modo de demonstração/teste. Antes de qualquer cobrança real, um
administrador deve confirmar as taxas vigentes na documentação oficial do
provedor escolhido e sobrescrever este config (ex.: carregando de um
painel administrativo ou variável de ambiente — não deste arquivo).
"""
from __future__ import annotations

from .models import CommissionBase, InstallmentInterestMode, PaymentFeeMode

# Sinalizador global: se True, qualquer taxa/valor abaixo é apenas ilustrativo
# e não deve ser usado para cobrar um cliente real.
ILUSTRATIVO = True

# -------- Taxas de gateway por método de pagamento --------
# Percentual cobrado pelo provedor sobre o valor da venda. Placeholder — a
# documentação oficial do provedor escolhido deve ser consultada antes de
# qualquer integração real (seção 31 — "TON — REGRA").
DEFAULT_GATEWAY_FEE_PERCENT = {
    "PIX": 0.0099,             # 0,99% — ilustrativo
    "CREDIT_AVISTA": 0.0399,   # 3,99% — ilustrativo
}

# -------- Taxa incremental por número de parcelas (cartão parcelado) --------
# Normalmente cresce com o número de parcelas. Placeholder ilustrativo — não
# é a tabela real de nenhum adquirente.
DEFAULT_INSTALLMENT_FEE_PERCENT = {
    1: 0.0399, 2: 0.0459, 3: 0.0519, 4: 0.0579, 5: 0.0639, 6: 0.0699,
    7: 0.0799, 8: 0.0859, 9: 0.0919, 10: 0.0979, 11: 0.1039, 12: 0.1099,
}

# -------- Tabela de juros repassados ao cliente (modo JUROS_DO_CLIENTE) --------
# Percentual adicional, por parcela, cobrado do cliente além da taxa de
# gateway — só é aplicado quando installment_interest_mode == JUROS_DO_CLIENTE.
# Ilustrativo — admin define a política real.
DEFAULT_CUSTOMER_INTEREST_PERCENT = {n: 0.0 for n in range(1, 13)}

DEFAULT_PAYMENT_FEE_MODE = PaymentFeeMode.MERCHANT_ABSORBS
DEFAULT_INSTALLMENT_INTEREST_MODE = InstallmentInterestMode.SEM_JUROS
DEFAULT_MAX_INSTALLMENTS = 12
DEFAULT_MIN_INSTALLMENT_VALUE = 50.0  # não fragmentar parcelas abaixo disso

# -------- Comissão de afiliado --------
DEFAULT_COMMISSION_RATE = 0.10           # 10% por venda — valor oficial atual do V2
DEFAULT_COMMISSION_BASE = CommissionBase.GROSS_ORDER
DEFAULT_COMMISSION_HOLD_DAYS = 30        # prazo de liberação — placeholder, admin define
DEFAULT_COMMISSION_MIN_PAYOUT = 100.0    # valor mínimo de saque — placeholder, admin define

# -------- Margem --------
DEFAULT_MINIMUM_MARGIN_PERCENTAGE = 0.35  # placeholder — admin define o mínimo real

# -------- Desconto Pix --------
DEFAULT_PIX_DISCOUNT_PERCENT = 0.0  # 0 = nenhum desconto automático; admin configura


def default_commerce_config() -> dict:
    """Retorna a configuração padrão (ilustrativa) como dict simples — o
    formato que um painel administrativo real substituiria por valores
    confirmados."""
    return {
        "ilustrativo": ILUSTRATIVO,
        "gateway_fee_percent": dict(DEFAULT_GATEWAY_FEE_PERCENT),
        "installment_fee_percent": dict(DEFAULT_INSTALLMENT_FEE_PERCENT),
        "customer_interest_percent": dict(DEFAULT_CUSTOMER_INTEREST_PERCENT),
        "payment_fee_mode": DEFAULT_PAYMENT_FEE_MODE,
        "installment_interest_mode": DEFAULT_INSTALLMENT_INTEREST_MODE,
        "max_installments": DEFAULT_MAX_INSTALLMENTS,
        "min_installment_value": DEFAULT_MIN_INSTALLMENT_VALUE,
        "commission_rate": DEFAULT_COMMISSION_RATE,
        "commission_base": DEFAULT_COMMISSION_BASE,
        "commission_hold_days": DEFAULT_COMMISSION_HOLD_DAYS,
        "commission_min_payout": DEFAULT_COMMISSION_MIN_PAYOUT,
        "minimum_margin_percentage": DEFAULT_MINIMUM_MARGIN_PERCENTAGE,
        "pix_discount_percent": DEFAULT_PIX_DISCOUNT_PERCENT,
        "hybrid_fee_split_customer": 0.5,  # só usado em payment_fee_mode HYBRID
    }
