# === Stage 1: Каркас модуля ===
# Project: FlashDeck
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Card:
    question: str
    answer: str
    deck: str
    date: date


def make_demo_cards() -> list:
    return [
        Card("Что означает HTTP?",
             "HyperText Transfer Protocol",
             "Основы",
             date(2024, 1, 15)),
        Card("Столица Франции?",
             "Париж",
             "География",
             date(2024, 1, 16)),
        Card("2 + 2",
             "4",
             "Математика",
             date(2024, 1, 17)),
    ]


def main() -> None:
    cards = make_demo_cards()
    print("FlashDeck — карточки для запоминания")
    print(f"Загружено колод: {len(set(c.deck for c in cards))}")
    print(f"Всего карточек: {len(cards)}")
    for card in cards:
        print(f"  [{card.deck}] {card.question} -> {card.answer} "
              f"(дата: {card.date.isoformat()})")


if __name__ == "__main__":
    main()
