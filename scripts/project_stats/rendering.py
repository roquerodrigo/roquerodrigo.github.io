from html import escape
from pathlib import Path

from .catalog import Project

STAR_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.94 6.26 6.56.63-4.94 4.46 '
    '1.42 6.45L12 16.9l-5.98 3.36 1.42-6.45L2.5 8.89l6.56-.63z"/></svg>'
)
DOWNLOAD_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"/></svg>'
)


def format_count(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def pluralize(value: int, singular: str, plural: str) -> str:
    return f"{format_count(value)} {singular if value == 1 else plural}"


class ProjectCardRenderer:
    INDENT = " " * 10

    def render_all(self, projects: list[Project]) -> str:
        return "\n\n".join(self.render(project) for project in projects)

    def render(self, project: Project) -> str:
        lines = [
            f'<a class="project" href="{escape(project.url)}" target="_blank" rel="noopener">',
            '  <div class="project__head">',
            f'    <span class="project__name mono">{escape(project.name)}</span>',
            f'    <span class="project__stars mono" aria-label="{pluralize(project.stars, "estrela", "estrelas")}">',
            f"      {STAR_ICON}{format_count(project.stars)}",
            "    </span>",
            "  </div>",
            f'  <p class="project__desc">{escape(project.description)}</p>',
            '  <div class="project__meta">',
            f'    <span class="project__tag">{escape(project.tag)}</span>',
            *self._downloads_lines(project),
            f'    <span class="project__lang"><span class="project__dot" style="--lang: {escape(project.language_color)}">'
            f"</span>{escape(project.language)}</span>",
            "  </div>",
            "</a>",
        ]
        return "\n".join(self.INDENT + line for line in lines)

    @staticmethod
    def _downloads_lines(project: Project) -> list[str]:
        if project.downloads is None:
            return []
        label = pluralize(project.downloads, "download", "downloads")
        return [
            f'    <span class="project__downloads mono" title="{label}" aria-label="{label}">',
            f"      {DOWNLOAD_ICON}{format_count(project.downloads)}",
            "    </span>",
        ]


class IndexPage:
    START_MARKER = "<!-- projects:start -->"
    END_MARKER = "<!-- projects:end -->"

    def __init__(self, path: Path) -> None:
        self.path = path

    def replace_projects(self, cards_html: str) -> None:
        page = self.path.read_text(encoding="utf-8")
        before, rest = page.split(self.START_MARKER, 1)
        _, after = rest.split(self.END_MARKER, 1)
        closing_indent = before[before.rfind("\n") + 1 :]
        updated = f"{before}{self.START_MARKER}\n{cards_html}\n{closing_indent}{self.END_MARKER}{after}"
        self.path.write_text(updated, encoding="utf-8")
