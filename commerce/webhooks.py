"""
webhooks.py — idempotência de eventos de pagamento (seções 33, 34 do adendo).

Este módulo NÃO recebe webhooks reais (não há servidor HTTP exposto neste
projeto — é um site estático). Ele modela a peça que qualquer backend real
precisaria: um armazenamento de eventos já processados, para que a mesma
notificação de pagamento nunca duplique pedido, comissão, projeto ou
assinatura (seção 34).

A implementação abaixo (`InMemoryIdempotencyStore`) é só para demonstração e
testes — uma implementação real usaria uma tabela de banco de dados com uma
constraint de unicidade em `event_id`.
"""
from __future__ import annotations

from .models import PaymentEvent


class DuplicateEventError(RuntimeError):
    """Levantado quando um evento com o mesmo event_id já foi processado."""


class IdempotencyStore:
    """Contrato mínimo que um armazenamento de idempotência precisa cumprir."""

    def has_processed(self, event_id: str) -> bool:
        raise NotImplementedError

    def mark_processed(self, event: PaymentEvent) -> None:
        raise NotImplementedError


class InMemoryIdempotencyStore(IdempotencyStore):
    """Implementação em memória — só para testes/demonstração. Uma
    implementação real precisa de persistência (banco de dados), porque este
    processo não roda continuamente como um servidor."""

    def __init__(self) -> None:
        self._seen: dict[str, PaymentEvent] = {}

    def has_processed(self, event_id: str) -> bool:
        return event_id in self._seen

    def mark_processed(self, event: PaymentEvent) -> None:
        self._seen[event.event_id] = event


def process_webhook_event(event: PaymentEvent, store: IdempotencyStore) -> PaymentEvent:
    """Processa um evento de webhook de forma idempotente: se o event_id já
    foi visto, levanta DuplicateEventError em vez de reprocessar (o
    chamador decide se isso é um erro ou um no-op silencioso)."""
    if store.has_processed(event.event_id):
        raise DuplicateEventError(
            f"Evento {event.event_id} já foi processado — ignorando para evitar "
            f"duplicar pedido/comissão/assinatura (seção 34)."
        )
    event.processed = True
    store.mark_processed(event)
    return event
