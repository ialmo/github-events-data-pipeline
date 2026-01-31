from typing import Any


def _parse_iso(dt: str | None) -> str | None:
    """
    GitHub já retorna ISO 8601 (ex: 2026-01-31T04:12:36Z).
    Para este projeto (SQLite), manter como string ISO é suficiente.
    """
    return dt if dt else None


def normalize_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Transforma a lista de eventos (JSON) em linhas tabulares (lista de dicts).
    Essa é a camada 'silver': dados limpos e com schema estável.
    """
    rows: list[dict[str, Any]] = []

    for e in events:
        actor = e.get("actor") or {}
        repo = e.get("repo") or {}

        rows.append(
            {
                "event_id": e.get("id"),
                "event_type": e.get("type"),
                "created_at": _parse_iso(e.get("created_at")),
                "actor_id": actor.get("id"),
                "actor_login": actor.get("login"),
                "repo_id": repo.get("id"),
                "repo_name": repo.get("name"),
                "public": e.get("public"),
            }
        )

    return rows
