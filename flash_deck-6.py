# === Stage 6: Связанная сущность ===
# Project: FlashDeck
import datetime
import uuid


def new_card_id():
    return str(uuid.uuid4())


def new_repeat_id():
    return str(uuid.uuid4())


class Card:
    def __init__(self, question, answer, deck, created=None):
        self.id = new_card_id()
        self.question = question
        self.answer = answer
        self.deck = deck
        self.created = created or datetime.date.today()

    def __repr__(self):
        return f"Card({self.id!r}, q={self.question!r}, d={self.deck!r})"


class Repeat:
    def __init__(self, card_id, due, interval, next_review=None):
        self.id = new_repeat_id()
        self.card_id = card_id
        self.due = due
        self.interval = interval
        self.next_review = next_review or due

    def __repr__(self):
        return f"Repeat({self.id!r}, card={self.card_id!r}, due={self.due!r})"


def add_repeat(repeats, card_id, due=None, interval=1):
    if card_id not in repeats:
        raise KeyError(f"Нет карточки с id={card_id}")
    if due is None:
        due = datetime.date.today()
    repeat = Repeat(card_id, due, interval)
    repeats[repeat.id] = repeat
    return repeat


def add_repeats(repeats, cards, due=None, interval=1):
    for card in cards:
        add_repeat(repeats, card.id, due, interval)
    return repeats
