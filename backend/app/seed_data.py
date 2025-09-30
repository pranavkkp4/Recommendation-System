from typing import List

from sqlalchemy.orm import Session

from . import models


ITEMS: List[dict] = [
    {
        "title": "The Pragmatic Programmer",
        "description": "A classic guide to pragmatic software craftsmanship.",
        "category": "Books",
        "tags": "software,programming,career",
    },
    {
        "title": "Clean Code",
        "description": "Best practices for writing clean, maintainable code.",
        "category": "Books",
        "tags": "software,engineering,craftsmanship",
    },
    {
        "title": "Inception",
        "description": "A mind-bending science fiction thriller by Christopher Nolan.",
        "category": "Movies",
        "tags": "science fiction,dreams,thriller",
    },
    {
        "title": "Interstellar",
        "description": "Exploring space and time to save humanity.",
        "category": "Movies",
        "tags": "science fiction,space,drama",
    },
    {
        "title": "The Alchemist",
        "description": "A philosophical tale about following one's dreams.",
        "category": "Books",
        "tags": "fiction,philosophy,inspiration",
    },
    {
        "title": "Noise Cancelling Headphones",
        "description": "Premium over-ear headphones with adaptive noise cancellation.",
        "category": "Products",
        "tags": "audio,electronics,comfort",
    },
    {
        "title": "Smart Fitness Watch",
        "description": "Track your workouts, sleep, and health metrics.",
        "category": "Products",
        "tags": "fitness,wearable,health",
    },
    {
        "title": "Parasite",
        "description": "Academy Award-winning social thriller from South Korea.",
        "category": "Movies",
        "tags": "thriller,drama,international",
    },
    {
        "title": "Atomic Habits",
        "description": "Build good habits and break bad ones with science-backed advice.",
        "category": "Books",
        "tags": "productivity,self-help,psychology",
    },
    {
        "title": "Ergonomic Office Chair",
        "description": "Comfortable office chair with lumbar support.",
        "category": "Products",
        "tags": "office,comfort,health",
    },
]


def seed_items(db: Session) -> None:
    if db.query(models.Item).first():
        return
    for item in ITEMS:
        db.add(models.Item(**item))
    db.commit()
