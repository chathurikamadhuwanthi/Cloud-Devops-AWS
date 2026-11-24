import os
import time
from contextlib import asynccontextmanager

import psycopg2
from fastapi import FastAPI


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "appuser"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def init_db():
    for _ in range(20):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS visits "
                "(id SERIAL PRIMARY KEY, ts TIMESTAMP DEFAULT NOW())"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError("Database is not reachable")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Cloud DevOps project is running on AWS"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/visits")
def visits():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"total_visits": count}
