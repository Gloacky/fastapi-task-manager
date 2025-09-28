To install run:
pip install -r requirements.txt

1. Copy `.env.example` → `.env`
2. Edit `.env` with your own database credentials
3. Run `alembic upgrade head` to create the tables
4. Start the app with `uvicorn app.main:app --reload`
