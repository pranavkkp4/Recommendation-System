from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np
from sqlalchemy.orm import Session

from . import crud, models


@dataclass
class RecommendationResult:
    item: models.Item
    score: float
    strategy: str


class RecommenderEngine:
    """Hybrid recommender supporting collaborative filtering and content-based matching."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_ratings(self) -> Dict[int, Dict[int, float]]:
        ratings_map: Dict[int, Dict[int, float]] = defaultdict(dict)
        ratings: Sequence[models.Rating] = self.db.query(models.Rating).all()
        for rating in ratings:
            ratings_map[rating.user_id][rating.item_id] = rating.score
        return ratings_map

    def collaborative_filtering(self, user_id: int, top_k: int = 10) -> List[Tuple[int, float]]:
        ratings = self.get_all_ratings()
        target_ratings = ratings.get(user_id, {})
        if not target_ratings:
            return []

        similarities: List[Tuple[int, float]] = []
        target_vector = self._vector_from_ratings(target_ratings)
        for other_user, other_ratings in ratings.items():
            if other_user == user_id or not other_ratings:
                continue
            other_vector = self._vector_from_ratings(other_ratings)
            score = self._cosine_similarity(target_vector, other_vector)
            if score > 0:
                similarities.append((other_user, score))
        if not similarities:
            return []

        ranked: Dict[int, float] = defaultdict(float)
        for other_user, similarity in similarities:
            for item_id, score in ratings[other_user].items():
                if item_id in target_ratings:
                    continue
                ranked[item_id] += similarity * score

        normalized = [(item_id, score) for item_id, score in ranked.items()]
        normalized.sort(key=lambda x: x[1], reverse=True)
        return normalized[:top_k]

    def content_based(self, user: models.User, top_k: int = 10) -> List[Tuple[int, float]]:
        items = crud.list_items(self.db)
        user_tags = self._collect_user_tags(user)
        if not user_tags:
            return []

        scored_items: List[Tuple[int, float]] = []
        for item in items:
            item_tags = self._tokenize_tags(item.tags)
            overlap = len(user_tags & item_tags)
            if overlap and not any(r.item_id == item.id for r in user.ratings):
                scored_items.append((item.id, float(overlap) / len(user_tags)))
        scored_items.sort(key=lambda x: x[1], reverse=True)
        return scored_items[:top_k]

    def hybrid(self, user: models.User, top_k: int = 10) -> List[RecommendationResult]:
        collaborative = self.collaborative_filtering(user.id, top_k=top_k)
        content_based = self.content_based(user, top_k=top_k)
        combined: Dict[int, Tuple[float, str]] = {}

        for item_id, score in collaborative:
            combined[item_id] = (score, "collaborative")
        for item_id, score in content_based:
            existing = combined.get(item_id)
            if existing:
                combined[item_id] = (existing[0] + score, "hybrid")
            else:
                combined[item_id] = (score, "content")

        if not combined:
            combined = {
                item.id: (self._popularity_score(item), "popular")
                for item in crud.list_items(self.db)
                if not any(r.item_id == item.id for r in user.ratings)
            }

        ranked = sorted(combined.items(), key=lambda x: x[1][0], reverse=True)[:top_k]
        results = [
            RecommendationResult(item=crud.get_item(self.db, item_id), score=score, strategy=strategy)
            for item_id, (score, strategy) in ranked
        ]
        return [res for res in results if res.item is not None]

    def _vector_from_ratings(self, ratings: Dict[int, float]) -> np.ndarray:
        if not ratings:
            return np.array([])
        sorted_items = sorted(ratings.keys())
        vector = np.array([ratings[item_id] for item_id in sorted_items])
        norm = np.linalg.norm(vector)
        return vector / norm if norm else vector

    @staticmethod
    def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        if vec_a.size == 0 or vec_b.size == 0:
            return 0.0
        min_len = min(len(vec_a), len(vec_b))
        vec_a = vec_a[:min_len]
        vec_b = vec_b[:min_len]
        numerator = float(np.dot(vec_a, vec_b))
        denominator = float(np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        return numerator / denominator if denominator else 0.0

    def _collect_user_tags(self, user: models.User) -> set[str]:
        explicit_tags = {pref.tag for pref in user.preferences}
        rated_tags = set()
        for rating in user.ratings:
            item_tags = self._tokenize_tags(rating.item.tags)
            rated_tags.update(item_tags)
        return explicit_tags | rated_tags

    @staticmethod
    def _tokenize_tags(tags: str | None) -> set[str]:
        if not tags:
            return set()
        return {tag.strip().lower() for tag in tags.split(",") if tag.strip()}

    def _popularity_score(self, item: models.Item) -> float:
        if not item.ratings:
            return 0.0
        avg_score = sum(r.score for r in item.ratings) / len(item.ratings)
        return avg_score


def build_recommendations(db: Session, user: models.User, top_k: int = 10) -> List[RecommendationResult]:
    engine = RecommenderEngine(db)
    return engine.hybrid(user=user, top_k=top_k)
