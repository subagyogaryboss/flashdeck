# === Stage 3: Хранилище в памяти ===
# Project: FlashDeck
import uuid
from datetime import datetime


class Card:
    """Карточка для запоминания.

    Поля: вопрос, ответ, колода, дата создания.
    Идентификатор генерируется автоматически.
    """

    def __init__(self, question, answer, deck, created=None):
        self.id = str(uuid.uuid4())
        self.question = question
        self.answer = answer
        self.deck = deck
        self.created = created or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "deck": self.deck,
            "created": self.created.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            answer=data["answer"],
            deck=data["deck"],
            created=datetime.fromisoformat(data["created"]),
        )

    def __repr__(self):
        return f"Card(id={self.id}, question={self.question!r})"


class InMemoryCardStore:
    """Хранилище карточек в памяти.

    Поддерживает добавление, получение по идентификатору и список.
    """

    def __init__(self):
        self._cards = {}

    def add_card(self, card):
        self._cards[card.id] = card
        return card

    def get_card(self, card_id):
        return self._cards.get(card_id)

    def list_cards(self, deck=None):
        if deck is None:
            return list(self._cards.values())
        return [card for card in self._cards.values() if card.deck == deck]

    def count(self, deck=None):
        cards = self.list_cards(deck)
        return len(cards)
