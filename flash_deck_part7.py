# === Stage 7: Связи между сущностями ===
# Project: FlashDeck
from datetime import datetime
from collections import defaultdict


def _parse_date(value):
    if value is None:
        return None
    return datetime.fromisoformat(value).date()


def get_all_repetitions_for_card(card, repetitions):
    card_id = card["id"]
    card_deck_id = card["deck_id"]
    card_due = _parse_date(card.get("due"))

    card_repetions = list(
        repetitions.get(card_id, [])
    )

    if card_due is None:
        due_repetitions = list(
            repetitions.get(card_deck_id, [])
        )
    else:
        due_repetitions = [
            repetition
            for repetition in repetitions.get(
                card_deck_id, []
            )
            if _parse_date(repetition["due"])
            <= card_due
        ]

    return card_repetions + due_repetitions


def check_card_repetition_integrity(card, repetitions):
    card_id = card["id"]
    card_deck_id = card["deck_id"]
    card_repetition_ids = set()

    for repetition in get_all_repetitions_for_card(
        card, repetitions
    ):
        card_repetition_ids.add(repetition["id"])

    orphan_repetitions = [
        repetition
        for repetition in repetitions.get(
            card_id, []
        )
        if repetition["id"] not in card_repetition_ids
    ]

    missing_repetition = [
        repetition
        for repetition in repetitions.get(
            card_deck_id, []
        )
        if (
            _parse_date(repetition["due"])
            <= _parse_date(card["due"])
            and repetition["id"]
            not in card_repetition_ids
        )
    ]

    return {
        "card_id": card_id,
        "deck_id": card_deck_id,
        "card_repetition_count": len(
            card_repetition_ids
        ),
        "orphan_repetitions": orphan_repetitions,
        "missing_repetitions": missing_repetition,
    }


def build_repetitions_by_card(repetitions):
    card_repetitions = defaultdict(list)

    for card_id in repetitions:
        for repetition in repetitions[card_id]:
            card_repetitions[card_id].append(
                repetition
            )

    return card_repetitions
