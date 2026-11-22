# === Stage 4: Редактирование записей ===
# Project: FlashDeck
from datetime import datetime
from typing import Any, Dict, Optional


class CardField:
    ALLOWED_FIELDS = ("question", "answer", "deck", "created_at")

    def __init__(self, question: str, answer: str, deck: str, created_at: Optional[datetime] = None):
        self.question = question
        self.answer = answer
        self.deck = deck
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer,
            "deck": self.deck,
            "created_at": self.created_at,
        }


class Card:
    def __init__(self, card_id: int, question: str, answer: str, deck: str, created_at: Optional[datetime] = None):
        self.id = card_id
        self.question = question
        self.answer = answer
        self.deck = deck
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "deck": self.deck,
            "created_at": self.created_at,
        }


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None or isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    return None


def _validate_deck(value: Any) -> bool:
    if isinstance(value, str) and value.strip():
        return True
    return False


def update_card(card: Card, payload: Dict[str, Any]) -> Dict[str, Any]:
    updated_fields: Dict[str, Any] = {}

    if "question" in payload and payload["question"] is not None:
        if isinstance(payload["question"], str):
            updated_fields["question"] = payload["question"]

    if "answer" in payload and payload["answer"] is not None:
        if isinstance(payload["answer"], str):
            updated_fields["answer"] = payload["answer"]

    if "deck" in payload:
        if _validate_deck(payload["deck"]):
            updated_fields["deck"] = payload["deck"]

    if "created_at" in payload:
        coerced = _coerce_datetime(payload["created_at"])
        if coerced is not None:
            updated_fields["created_at"] = coerced

    for field in CardField.ALLOWED_FIELDS:
        if field in updated_fields:
            setattr(card, field, updated_fields[field])

    return card.to_dict()
