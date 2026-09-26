import os
import sys
from pathlib import Path

from .catalog import Project, ProjectCatalog
from .rendering import IndexPage, ProjectCardRenderer
from .sources import DownloadCounter, GitHubRepositories, HttpClient

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def refresh(project: Project, github: GitHubRepositories, downloads: DownloadCounter) -> bool:
    succeeded = True
    try:
        project.stars = github.stars(project.repository)
    except Exception as error:
        print(f"::warning::keeping previous stars for {project.repository}: {error}", file=sys.stderr)
        succeeded = False
    if project.package:
        try:
            project.downloads = downloads.total(project.package)
        except Exception as error:
            print(f"::warning::keeping previous downloads for {project.repository}: {error}", file=sys.stderr)
            succeeded = False
    return succeeded


def main() -> int:
    http = HttpClient(github_token=os.environ.get("GITHUB_TOKEN"))
    github = GitHubRepositories(http)
    downloads = DownloadCounter(http)
    catalog = ProjectCatalog(REPOSITORY_ROOT / "data" / "projects.json")

    projects = catalog.load()
    results = [refresh(project, github, downloads) for project in projects]
    projects.sort(key=lambda project: (-project.stars, -(project.downloads or 0)))

    catalog.save(projects)
    IndexPage(REPOSITORY_ROOT / "site" / "index.html").replace_projects(ProjectCardRenderer().render_all(projects))

    for project in projects:
        print(f"{project.name}: {project.stars} stars, {project.downloads} downloads")
    return 0 if any(results) else 1


if __name__ == "__main__":
    sys.exit(main())
