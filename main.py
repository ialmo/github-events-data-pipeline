import json
import sqlite3
from pathlib import Path

from src.settings import Settings
from src.ingest_github import fetch_events, save_raw_json
from src.transform import normalize_events
from src.load_sqlite import upsert_events


def main():
    settings = Settings()

    # 1) INGEST
    events = fetch_events(settings)
    raw_path = save_raw_json(settings, events)

    # 2) TRANSFORM
    rows = normalize_events(events)

    # 3) LOAD
    upsert_events(settings, rows)

    # 4) CHECKS
    with sqlite3.connect(settings.sqlite_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM events;").fetchone()[0]
        top = conn.execute(
            """
            SELECT event_type, COUNT(*) c
            FROM events
            GROUP BY event_type
            ORDER BY c DESC
            LIMIT 5;
            """
        ).fetchall()

    print("PIPELINE EXECUTADO COM SUCESSO")
    print("RAW:", raw_path)
    print("SQLite:", settings.sqlite_path)
    print("Total eventos:", total)
    print("Top 5 tipos:", top)


if __name__ == "__main__":
    main()
