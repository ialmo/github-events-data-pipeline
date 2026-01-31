import json
import time
from datetime import datetime, timezone
from typing import Any

import requests

from .settings import Settings


def _utc_now_compact() -> str:
    """
    Retorna timestamp UTC compacto para versionar arquivos raw.
    Ex: 20260131T003012Z
    """
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fetch_events(settings: Settings) -> list[dict[str, Any]]:
    """
    Busca eventos do repositório via GitHub API.
    """
    url = f"https://api.github.com/repos/{settings.owner}/{settings.repo}/events"
    params = {"per_page": settings.per_page}
    headers = {"Accept": "application/vnd.github+json"}

    for attempt in range(1, 4):
        response = requests.get(url, params=params, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()

        # Rate limit ou erro temporário
        if response.status_code in (403, 429):
            time.sleep(2 * attempt)
            continue

        time.sleep(attempt)

    response.raise_for_status()
    return []


def save_raw_json(settings: Settings, events: list[dict[str, Any]]) -> str:
    """
    Salva os eventos brutos em JSON versionado por timestamp.
    """
    settings.raw_dir.mkdir(parents=True, exist_ok=True)

    output_path = settings.raw_dir / f"github_events_{_utc_now_compact()}.json"

    output_path.write_text(
        json.dumps(events, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return str(output_path)
