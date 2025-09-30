# Personalized Recommender System

This project showcases an end-to-end personalized recommendation platform. It combines a FastAPI backend, a hybrid (collaborative + content-based) machine learning engine, a React single-page application, and a relational database for persistent storage.

## Features

- **User accounts** – Register, authenticate, and manage personal preference tags.
- **Item catalog** – Books, movies, and products stored in SQL with descriptive metadata.
- **Ratings** – Capture explicit 1–5 star feedback to learn user tastes.
- **Hybrid recommendations** – Blend collaborative filtering similarities with content-based signals and popularity fallback.
- **Activity history** – Review past ratings and log generated recommendation batches.
- **Modern UI** – React + Vite front-end for browsing, rating, and tuning interests.

## Tech stack

| Layer          | Technology |
| -------------- | ---------- |
| Frontend       | React 18, Vite, Axios |
| Backend        | FastAPI, SQLAlchemy |
| Database       | SQLite (easily replaceable with PostgreSQL/MySQL) |
| Machine learning | NumPy-powered collaborative & content-based hybrid |
| Auth           | OAuth2 password flow with JWT tokens |

## Getting started

### Backend

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Launch the FastAPI server:

   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

   The server seeds the SQLite database with the sample catalog on startup.

### Frontend

1. Install Node.js 18+.
2. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

3. Run the development server:

   ```bash
   npm run dev
   ```

4. Open the React app at `http://localhost:5173`. Set `VITE_API_BASE_URL` in a `.env` file if the backend runs on a different host.

### Production build

- Create a production bundle with `npm run build`.
- Deploy the FastAPI app with a production ASGI server (e.g., Uvicorn + Gunicorn) and back it with a managed SQL database.

## Architecture overview

```
frontend/            # React SPA served by Vite
  src/
    components/      # UI widgets for login, catalog, recommendations, etc.
    hooks/           # Authentication context
    api.js           # Axios client with token injection
backend/
  app/
    main.py          # FastAPI application and HTTP routes
    models.py        # SQLAlchemy ORM models
    schemas.py       # Pydantic DTOs
    recommender.py   # Hybrid recommendation engine
    seed_data.py     # Sample catalog bootstrap
    auth.py          # JWT helpers and security dependencies
    crud.py          # Database access helpers
    config.py        # Centralized configuration
  requirements.txt
```

The recommendation engine builds collaborative similarities from stored ratings, enriches the results with content-based tag overlaps, and falls back to popularity when little data is available. Recommendation batches are logged per user to support analytics.

## Future enhancements

- Swap SQLite for PostgreSQL and add Alembic migrations.
- Add implicit feedback signals (clicks, wishlist) and time decay.
- Integrate background jobs for offline model training.
- Provide evaluation dashboards and A/B testing support.
- Containerize the stack with Docker Compose for easier deployment.

## License

This repository is released under the MIT License. See [LICENSE](LICENSE) for details.
