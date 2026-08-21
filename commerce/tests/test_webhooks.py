import pytest

from commerce.models import PaymentEvent
from commerce.webhooks import DuplicateEventError, InMemoryIdempotencyStore, process_webhook_event


def make_event(event_id="evt-1"):
    return PaymentEvent(
        event_id=event_id, provider="ton", event_type="payment.approved",
        order_id="ord-1", raw_payload={"status": "approved"},
    )


def test_first_event_processed_successfully():
    store = InMemoryIdempotencyStore()
    event = process_webhook_event(make_event(), store)
    assert event.processed is True
    assert store.has_processed("evt-1") is True


def test_duplicate_event_rejected():
    store = InMemoryIdempotencyStore()
    process_webhook_event(make_event("evt-2"), store)
    with pytest.raises(DuplicateEventError):
        process_webhook_event(make_event("evt-2"), store)


def test_different_events_both_processed():
    store = InMemoryIdempotencyStore()
    process_webhook_event(make_event("evt-3"), store)
    process_webhook_event(make_event("evt-4"), store)
    assert store.has_processed("evt-3")
    assert store.has_processed("evt-4")
