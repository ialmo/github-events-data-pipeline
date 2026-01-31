import sqlite3
from typing import Any

from .settings import Settings

DDL = """
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT,
  created_at TEXT,
  actor_id INTEGER,
  actor_login TEXT,
  repo_id INTEGER,
  repo_name TEXT,
  public INTEGER
);
"""


def upsert_events(settings: Settings, rows: list[dict[str, Any]]) -> None:
    """
    Cria a tabela (se não existir) e faz upsert por event_id.
    Idempotente: rodar 2x não duplica.
    """
    settings.processed_dir.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(settings.sqlite_path) as conn:
        conn.execute(DDL)

        # boas práticas para SQLite (melhor performance / concorrência)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

        conn.executemany(
            """
            INSERT INTO events (
              event_id, event_type, created_at, actor_id, actor_login, repo_id, repo_name, public
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
              event_type=excluded.event_type,
              created_at=excluded.created_at,
              actor_id=excluded.actor_id,
              actor_login=excluded.actor_login,
              repo_id=excluded.repo_id,
              repo_name=excluded.repo_name,
              public=excluded.public;
            """,
            [
                (
                    r["event_id"],
                    r["event_type"],
                    r["created_at"],
                    r["actor_id"],
                    r["actor_login"],
                    r["repo_id"],
                    r["repo_name"],
                    1 if r["public"] else 0,
                )
                for r in rows
            ],
        )
        conn.commit()
