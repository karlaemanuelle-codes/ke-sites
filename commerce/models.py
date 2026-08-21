"""
models.py — entidades centrais do motor comercial da KE Sites.

Todas as entidades são dataclasses simples (sem ORM, sem banco de dados —
este projeto não tem backend). Servem como o contrato de dados que uma
implementação real (com banco de dados de verdade) deveria seguir.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums — status e modos de configuração (seções 2, 10, 16, 18 do adendo)
# ---------------------------------------------------------------------------

class PaymentFeeMode(str, Enum):
    """Quem absorve a taxa do gateway de pagamento."""
    MERCHANT_ABSORBS = "MERCHANT_ABSORBS"
    CUSTOMER_PAYS = "CUSTOMER_PAYS"
    HYBRID = "HYBRID"


class InstallmentInterestMode(str, Enum):
    """Como os juros do parcelamento são tratados."""
    SEM_JUROS = "SEM_JUROS"
    JUROS_DO_CLIENTE = "JUROS_DO_CLIENTE"
    CONFIGURAVEL = "CONFIGURAVEL"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    APPROVED = "APPROVED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"


class SubscriptionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELLED = "CANCELLED"
    PAUSED = "PAUSED"
    EXPIRED = "EXPIRED"


class CommissionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    ADJUSTED = "ADJUSTED"
    PAID = "PAID"


class CommissionBase(str, Enum):
    """Sobre qual valor a comissão do afiliado é calculada (seção 16)."""
    GROSS_ORDER = "GROSS_ORDER"
    NET_ORDER = "NET_ORDER"
    CUSTOM = "CUSTOM"


class PromotionType(str, Enum):
    PERCENTAGE_DISCOUNT = "PERCENTAGE_DISCOUNT"
    FIXED_DISCOUNT = "FIXED_DISCOUNT"
    LAUNCH_PRICE = "LAUNCH_PRICE"
    COUPON = "COUPON"
    BUNDLE = "BUNDLE"
    UPGRADE_BONUS = "UPGRADE_BONUS"
    MAINTENANCE_BONUS = "MAINTENANCE_BONUS"
    REFERRAL_BONUS = "REFERRAL_BONUS"
    FIRST_PURCHASE = "FIRST_PURCHASE"
    LIMITED_TIME = "LIMITED_TIME"
    CUSTOM = "CUSTOM"


class PaymentMethod(str, Enum):
    PIX = "PIX"
    CREDIT_AVISTA = "CREDIT_AVISTA"
    CREDIT_PARCELADO = "CREDIT_PARCELADO"
    MANUAL_PIX = "MANUAL_PIX"
    MANUAL_TRANSFERENCIA = "MANUAL_TRANSFERENCIA"
    MANUAL_OUTRO = "MANUAL_OUTRO"


# ---------------------------------------------------------------------------
# Entidades (seções 11, 18, 10, 19, 12)
# ---------------------------------------------------------------------------

@dataclass
class Order:
    id: str
    customer_id: str
    template_id: str
    plan_id: str
    market: str                     # "BR" | "ES" | "US"
    currency: str                   # "BRL" | "EUR" | "USD"
    subtotal: float
    discount: float = 0.0
    payment_fee: float = 0.0
    installment_count: int = 1
    installment_value: float = 0.0
    total: float = 0.0
    payment_provider: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    affiliate_id: Optional[str] = None
    seller_id: Optional[str] = None
    partner_id: Optional[str] = None
    promotion_code: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Subscription:
    id: str
    customer_id: str
    plan_id: str                    # essencial | profissional | premium
    amount: float
    currency: str
    provider: Optional[str] = None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    start_date: Optional[str] = None
    next_billing_date: Optional[str] = None
    cancelled_at: Optional[str] = None


@dataclass
class Promotion:
    id: str
    name: str
    description: str
    code: Optional[str]
    type: PromotionType
    value: float
    currency: Optional[str]
    market: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    usage_limit: Optional[int]
    per_customer_limit: Optional[int]
    eligible_plans: list = field(default_factory=list)
    eligible_templates: list = field(default_factory=list)
    eligible_customers: list = field(default_factory=list)
    active: bool = False            # nunca ativa por padrão — admin decide (seção 12)
    stackable: bool = False
    created_at: Optional[str] = None


@dataclass
class Bonus:
    name: str
    description: str
    value: Optional[float]
    eligibility: str
    active: bool = False
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class Commission:
    id: str
    order_id: str
    affiliate_id: str
    base_amount: float
    commission_base: CommissionBase
    rate: float
    amount: float
    status: CommissionStatus = CommissionStatus.PENDING
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PaymentEvent:
    """Registro de um evento de webhook recebido — usado para idempotência
    (seção 34). `event_id` deve ser o id que o provedor atribui ao evento."""
    event_id: str
    provider: str
    event_type: str                 # payment.approved, subscription.cancelled, ...
    order_id: Optional[str]
    raw_payload: dict
    processed: bool = False
    received_at: Optional[str] = None
