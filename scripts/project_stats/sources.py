import json
import re
from datetime import date, datetime, timedelta
from urllib.parse import quote
from urllib.request import Request, urlopen

from .catalog import Package

USER_AGENT = "rodrigoroque.dev project-stats"


class HttpClient:
    def __init__(self, github_token: str | None = None) -> None:
        self.github_token = github_token

    def get_json(self, url: str):
        return json.loads(self.get_text(url))

    def get_text(self, url: str) -> str:
        request = Request(url, headers=self._headers_for(url))
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")

    def _headers_for(self, url: str) -> dict[str, str]:
        headers = {"User-Agent": USER_AGENT}
        if url.startswith("https://api.github.com/"):
            headers["Accept"] = "application/vnd.github+json"
            if self.github_token:
                headers["Authorization"] = f"Bearer {self.github_token}"
        return headers


class GitHubRepositories:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def stars(self, repository: str) -> int:
        return self.http.get_json(f"https://api.github.com/repos/{repository}")["stargazers_count"]

    def release_asset_downloads(self, repository: str) -> int:
        total = 0
        page = 1
        while releases := self.http.get_json(
            f"https://api.github.com/repos/{repository}/releases?per_page=100&page={page}"
        ):
            total += sum(asset["download_count"] for release in releases for asset in release["assets"])
            page += 1
        return total


class PyPIDownloads:
    BADGE_URL = "https://static.pepy.tech/personalized-badge/{name}?units=none&period=total"

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def total(self, name: str) -> int:
        badge = self.http.get_text(self.BADGE_URL.format(name=quote(name)))
        counts = re.findall(r">(\d+)</text>", badge)
        if not counts:
            raise ValueError(f"no download count found in the pepy badge for {name}")
        return int(counts[-1])


class NpmDownloads:
    MAXIMUM_RANGE = timedelta(days=540)

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    def total(self, name: str) -> int:
        created = self.http.get_json(f"https://registry.npmjs.org/{quote(name, safe='@')}")["time"]["created"]
        start = datetime.fromisoformat(created.replace("Z", "+00:00")).date()
        today = date.today()
        total = 0
        while start <= today:
            end = min(start + self.MAXIMUM_RANGE, today)
            total += self.http.get_json(
                f"https://api.npmjs.org/downloads/point/{start}:{end}/{quote(name, safe='@')}"
            )["downloads"]
            start = end + timedelta(days=1)
        return total


class DownloadCounter:
    def __init__(self, http: HttpClient) -> None:
        github = GitHubRepositories(http)
        self._counters = {
            "pypi": PyPIDownloads(http).total,
            "npm": NpmDownloads(http).total,
            "github-releases": github.release_asset_downloads,
        }

    def total(self, package: Package) -> int:
        return self._counters[package.registry](package.name)
