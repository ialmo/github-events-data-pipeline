from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """
    Configurações centrais do projeto.
    """

    # Fonte de dados (GitHub API)
    owner: str = "python"
    repo: str = "cpython"
    per_page: int = 50

    # Diretórios do projeto
    base_dir: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = base_dir / "data"
    raw_dir: Path = data_dir / "raw"
    processed_dir: Path = data_dir / "processed"

    # Banco local
    sqlite_path: Path = processed_dir / "events.sqlite"
