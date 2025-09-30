from datetime import datetime, timedelta
from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, crud, models, recommender, schemas, seed_data
from .auth import create_access_token, get_password_hash, verify_password
from .config import settings
from .database import Base, SessionLocal, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    db = SessionLocal()
    try:
        seed_data.seed_items(db)
    finally:
        db.close()


@app.post("/auth/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    created_user = crud.create_user(db, user=user, password_hash=hashed_password)
    return created_user


@app.post("/auth/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return schemas.Token(access_token=access_token)


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.get("/items", response_model=List[schemas.Item])
def list_items(db: Session = Depends(get_db)):
    return crud.list_items(db)


@app.post("/ratings", response_model=schemas.Rating)
def rate_item(
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_rating = crud.create_rating(db, user_id=current_user.id, rating=rating)
    return db_rating


@app.get("/ratings/me", response_model=List[schemas.Rating])
def read_my_ratings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_user_ratings(db, user_id=current_user.id)


@app.post("/users/me/preferences", response_model=schemas.User)
def update_preferences(
    tags: List[str] = Body(..., embed=True, description="List of preference tags such as genres or topics"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    crud.upsert_preference_tags(db, current_user, tags)
    db.refresh(current_user)
    return current_user


@app.get("/recommendations", response_model=schemas.RecommendationResponse)
def get_recommendations(
    top_k: int = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    results = recommender.build_recommendations(db, current_user, top_k=top_k)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recommendations available yet")
    crud.create_recommendation_log(db, current_user, strategy=results[0].strategy, recommended_ids=[res.item.id for res in results])
    return schemas.RecommendationResponse(
        recommendations=[
            schemas.Recommendation(item=res.item, score=res.score, strategy=res.strategy)
            for res in results
        ],
        generated_at=datetime.utcnow(),
    )
