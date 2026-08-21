"""
promotions.py — motor de promoções + proteção de margem (seções 10, 11, 62,
63, 64 do adendo).

Regra central: uma promoção nunca é aplicada automaticamente sem
elegibilidade explícita, e o motor calcula a margem líquida estimada antes
de permitir a promoção — se ficar abaixo do mínimo configurado, o sistema
sinaliza que a promoção exige aprovação administrativa (não bloqueia o
teste, apenas alerta — seção 64).
"""
from __future__ import annotations

from dataclasses import dataclass

from .models import Promotion


@dataclass(frozen=True)
class EligibilityContext:
    template_id: str
    plan_id: str
    market: str
    customer_id: str | None = None
    coupon_code: str | None = None


@dataclass(frozen=True)
class MarginCheck:
    gross_amount: float
    discount_amount: float
    gateway_fee_amount: float
    commission_amount: float
    other_costs: float
    net_revenue: float
    margin_percentage: float
    minimum_required: float
    requires_admin_approval: bool


def is_promotion_eligible(promotion: Promotion, ctx: EligibilityContext) -> bool:
    """Verifica elegibilidade — não aplica desconto, apenas responde sim/não
    (seção 62 — 'Não aplicar descontos incompatíveis')."""
    if not promotion.active:
        return False
    if promotion.code and promotion.code != ctx.coupon_code:
        return False
    if promotion.eligible_templates and ctx.template_id not in promotion.eligible_templates:
        return False
    if promotion.eligible_plans and ctx.plan_id not in promotion.eligible_plans:
        return False
    if promotion.market and promotion.market != ctx.market:
        return False
    if promotion.eligible_customers and ctx.customer_id not in promotion.eligible_customers:
        return False
    return True


def apply_promotion(*, amount: float, promotion: Promotion) -> float:
    """Aplica o desconto de uma promoção já validada como elegível. Não
    decide elegibilidade — chame is_promotion_eligible() antes."""
    if promotion.type.value == "PERCENTAGE_DISCOUNT":
        discount = amount * (promotion.value / 100.0 if promotion.value > 1 else promotion.value)
    elif promotion.type.value in ("FIXED_DISCOUNT", "LAUNCH_PRICE", "COUPON"):
        discount = promotion.value if promotion.type.value != "LAUNCH_PRICE" else max(0.0, amount - promotion.value)
    else:
        # Tipos como BUNDLE/UPGRADE_BONUS/REFERRAL_BONUS não são um simples
        # desconto percentual/fixo — exigem lógica própria fora deste helper.
        raise ValueError(
            f"Tipo de promoção '{promotion.type}' não é um desconto simples — "
            f"aplique a lógica específica desse tipo antes de chamar apply_promotion()."
        )
    discount = max(0.0, min(discount, amount))
    return round(amount - discount, 2)


def check_margin(
    *,
    gross_amount: float,
    discount_amount: float,
    gateway_fee_amount: float,
    commission_amount: float,
    other_costs: float,
    config: dict,
) -> MarginCheck:
    """Calcula a margem líquida estimada de uma venda com uma promoção
    aplicada e sinaliza se ela precisa de aprovação administrativa
    (seções 63-64). Nunca bloqueia — apenas informa."""
    net_revenue = round(
        gross_amount - discount_amount - gateway_fee_amount - commission_amount - other_costs, 2
    )
    margin_percentage = round(net_revenue / gross_amount, 4) if gross_amount else 0.0
    minimum_required = config.get("minimum_margin_percentage", 0.0)
    return MarginCheck(
        gross_amount=gross_amount,
        discount_amount=discount_amount,
        gateway_fee_amount=gateway_fee_amount,
        commission_amount=commission_amount,
        other_costs=other_costs,
        net_revenue=net_revenue,
        margin_percentage=margin_percentage,
        minimum_required=minimum_required,
        requires_admin_approval=margin_percentage < minimum_required,
    )
