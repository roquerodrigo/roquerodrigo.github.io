import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Package:
    registry: str
    name: str


@dataclass
class Project:
    repository: str
    description: str
    tag: str
    language: str
    language_color: str
    package: Package | None
    stars: int
    downloads: int | None

    @property
    def name(self) -> str:
        return self.repository.split("/")[-1]

    @property
    def url(self) -> str:
        return f"https://github.com/{self.repository}"


class ProjectCatalog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Project]:
        entries = json.loads(self.path.read_text(encoding="utf-8"))
        return [self._to_project(entry) for entry in entries]

    def save(self, projects: list[Project]) -> None:
        entries = [asdict(project) for project in projects]
        self.path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @staticmethod
    def _to_project(entry: dict) -> Project:
        package = entry.get("package")
        return Project(**{**entry, "package": Package(**package) if package else None})
