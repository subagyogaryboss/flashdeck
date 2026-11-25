# === Stage 5: Удаление и восстановление ===
# Project: FlashDeck
import datetime
from typing import List, Optional, Dict


class SoftDeletable:
    """Базовый класс с мягкой моделью удаления.

    Сущность помечается как удалённая, но остаётся в хранилище.
    Удаление не обратимо напрямую через флаги, но позволяет
    перемещать объект в состояние «восстановлен».
    """

    def __init__(self, id: str, deleted: bool = False):
        self.id = id
        self.deleted = deleted

    def is_deleted(self) -> bool:
        return self.deleted

    def delete(self) -> None:
        self.deleted = True

    def restore(self) -> None:
        self.deleted = False


class Card(SoftDeletable):
    """Карточка для запоминания.

    Поля: вопрос, ответ, колода, дата создания.
    Поддерживает мягкое удаление с восстановлением.
    """

    def __init__(self, id: str, question: str, answer: str,
                 deck_id: str, created_at: Optional[datetime.datetime] = None):
        super().__init__(id)
        self.question = question
        self.answer = answer
        self.deck_id = deck_id
        self.created_at = created_at or datetime.datetime.now()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "deck_id": self.deck_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deleted": self.deleted,
        }

    def soft_delete(self) -> None:
        self.delete()

    def restore(self) -> None:
        self.restore()


class CardRepository:
    """Хранилище карточек с поддержкой мягкого удаления.

    Все операции работают с объектами Card. Удаление не извлекает
    данные из памяти, а помечает их как удалённые, что позволяет
    выполнить восстановление позже.
    """

    def __init__(self):
        self._cards: Dict[str, Card] = {}

    def add(self, card: Card) -> Card:
        self._cards[card.id] = card
        return card

    def get(self, card_id: str) -> Optional[Card]:
        card = self._cards.get(card_id)
        return card if card and not card.is_deleted() else None

    def list_active(self) -> List[Card]:
        return [c for c in self._cards.values() if not c.is_deleted()]

    def list_all(self) -> List[Card]:
        return list(self._cards.values())

    def soft_delete(self, card_id: str) -> bool:
        card = self._cards.get(card_id)
        if card is None:
            return False
        card.soft_delete()
        return True

    def restore(self, card_id: str) -> bool:
        card = self._cards.get(card_id)
        if card is None or not card.is_deleted():
            return False
        card.restore()
