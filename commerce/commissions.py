"""
commissions.py — motor de comissão de afiliado (seções 12, 13, 16 do adendo).

Ciclo de vida (seção 12):
    CLICK -> LEAD -> ORDER -> PAYMENT APPROVED -> COMMISSION CREATED
    -> COMMISSION PENDING -> COMMISSION APPROVED -> PAYOUT

Regra central: a comissão NUNCA é calculada a partir de um clique — só a
partir de uma venda com pagamento aprovado (seção 12). Cancelamento/estorno
cancela ou ajusta a comissão correspondente (seção 13) — nunca paga
comissão de venda definitivamente cancelada.
"""
from __future__ import annotations

from .models import Commission, CommissionBase, CommissionStatus, Order, PaymentStatus


def create_commission_for_order(
    *, order: Order, config: dict, commission_id: str, created_at: str | None = None
) -> Commission | None:
    """Cria a comissão de um pedido — só deve ser chamado quando
    order.payment_status == APPROVED (o próprio pedido registra o clique/lead
    de origem via affiliate_id, mas a comissão só nasce após a aprovação)."""
    if not order.affiliate_id:
        return None
    if order.payment_status != PaymentStatus.APPROVED:
        raise ValueError(
            "Comissão só pode ser criada para pedidos com pagamento aprovado "
            f"(status atual: {order.payment_status})."
        )

    commission_base: CommissionBase = config["commission_base"]
    if commission_base == CommissionBase.GROSS_ORDER:
        base_amount = order.subtotal - order.discount
    elif commission_base == CommissionBase.NET_ORDER:
        base_amount = order.total - order.payment_fee
    elif commission_base == CommissionBase.CUSTOM:
        # Base customizada exige que o admin informe a lógica — não decidimos
        # automaticamente (seção 16: "Não decidir automaticamente sem
        # configuração"). Sem uma função customizada configurada, falha alto.
        custom_fn = config.get("custom_commission_base_fn")
        if custom_fn is None:
            raise ValueError(
                "commission_base=CUSTOM requer 'custom_commission_base_fn' no config."
            )
        base_amount = custom_fn(order)
    else:
        raise ValueError(f"commission_base desconhecido: {commission_base}")

    rate = config["commission_rate"]
    amount = round(base_amount * rate + 1e-9, 2)

    return Commission(
        id=commission_id,
        order_id=order.id,
        affiliate_id=order.affiliate_id,
        base_amount=round(base_amount, 2),
        commission_base=commission_base,
        rate=rate,
        amount=amount,
        status=CommissionStatus.PENDING,
        created_at=created_at,
    )


def approve_commission(commission: Commission) -> Commission:
    if commission.status != CommissionStatus.PENDING:
        raise ValueError(f"Só é possível aprovar comissão PENDING (atual: {commission.status})")
    commission.status = CommissionStatus.APPROVED
    return commission


def cancel_commission(commission: Commission, *, reason: str | None = None) -> Commission:
    """Cancela a comissão de uma venda cancelada/estornada (seção 13).
    Comissões já pagas não podem ser canceladas retroativamente por este
    método — isso exigiria uma política de cobrança/estorno de comissão,
    que fica fora de escopo aqui."""
    if commission.status == CommissionStatus.PAID:
        raise ValueError(
            "Comissão já paga — cancelamento retroativo exige política "
            "administrativa própria, não coberta por este método."
        )
    commission.status = CommissionStatus.CANCELLED
    return commission


def adjust_commission(commission: Commission, *, new_amount: float) -> Commission:
    """Ajusta o valor de uma comissão (ex.: estorno parcial) em vez de
    cancelá-la totalmente (seção 13 — 'CANCELADA ou AJUSTADA')."""
    if commission.status == CommissionStatus.PAID:
        raise ValueError("Comissão já paga não pode ser ajustada por este método.")
    commission.amount = round(new_amount, 2)
    commission.status = CommissionStatus.ADJUSTED
    return commission


def eligible_for_payout(commission: Commission, *, config: dict) -> bool:
    """Uma comissão só é elegível para saque se aprovada e acima do valor
    mínimo configurado (seção 12 — 'valor mínimo de saque')."""
    return (
        commission.status == CommissionStatus.APPROVED
        and commission.amount >= config.get("commission_min_payout", 0.0)
    )
