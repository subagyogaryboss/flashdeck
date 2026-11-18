# === Stage 2: Проверка полей ===
# Project: FlashDeck
import re
from datetime import date


def normalize_text(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value.strip())


def normalize_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    text = normalize_text(value)
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return date.fromisoformat(text)
        except ValueError:
            continue
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            parsed = date(*map(int, re.split(r"[/.-]", text)))
            return date(parsed.year, parsed.month, parsed.day)
        except (ValueError, TypeError):
            continue
    return None


def normalize_deck(value):
    if value is None:
        return ""
    text = normalize_text(value).lower()
    if not text:
        return ""
    text = re.sub(r"[^a-zа-яё0-9 _-]", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text.strip())


def validate_card(card):
    errors = []

    question = normalize_text(card.get("question"))
    if not question:
        errors.append("Поле 'вопрос' не может быть пустым")

    answer = normalize_text(card.get("answer"))
    if not answer:
        errors.append("Поле 'ответ' не может быть пустым")

    deck = normalize_deck(card.get("deck"))
    if not deck:
        errors.append("Поле 'колода' не может быть пустым")

    raw_date = card.get("date")
    if raw_date is None:
        errors.append("Поле 'дата' не может быть пустым")
    card_date = normalize_date(raw_date)
    if card_date is None:
        errors.append("Неверный формат даты 'дата'. Ожидается, например, 2024-01-15")
    else:
        card["date"] = card_date

    card["question"] = question
    card["answer"] = answer
    card["deck"] = deck

    return errors
