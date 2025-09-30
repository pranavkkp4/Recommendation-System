from typing import Iterable, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate, password_hash: str) -> models.User:
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(func.lower(models.User.email) == email.lower()).first()


def create_rating(db: Session, user_id: int, rating: schemas.RatingCreate) -> models.Rating:
    db_rating = (
        db.query(models.Rating)
        .filter(and_(models.Rating.user_id == user_id, models.Rating.item_id == rating.item_id))
        .first()
    )
    if db_rating:
        db_rating.score = rating.score
    else:
        db_rating = models.Rating(user_id=user_id, item_id=rating.item_id, score=rating.score)
        db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_user_ratings(db: Session, user_id: int) -> List[models.Rating]:
    return (
        db.query(models.Rating)
        .filter(models.Rating.user_id == user_id)
        .order_by(models.Rating.created_at.desc())
        .all()
    )


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def list_items(db: Session) -> List[models.Item]:
    return db.query(models.Item).order_by(models.Item.title.asc()).all()


def upsert_preference_tags(db: Session, user: models.User, tags: Iterable[str]) -> None:
    existing = {pref.tag for pref in user.preferences}
    for tag in existing - set(tags):
        pref = next(pref for pref in user.preferences if pref.tag == tag)
        db.delete(pref)
    for tag in set(tags) - existing:
        db.add(models.PreferenceTag(tag=tag, user=user))
    db.commit()


def create_recommendation_log(db: Session, user: models.User, strategy: str, recommended_ids: List[int]) -> models.RecommendationLog:
    log = models.RecommendationLog(
        user=user,
        strategy=strategy,
        recommended_items=",".join(str(i) for i in recommended_ids),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
