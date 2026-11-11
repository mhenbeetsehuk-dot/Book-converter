"""Read-only public research discovery using standard-library HTTP.

No credentials, shell execution, installation, cloning, or downloaded code execution.
"""
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER_AGENT = "Book-converter-research/0.1 (public metadata; human-reviewed)"
TIMEOUT = 12

def _json_get(base: str, params: dict) -> dict:
    url = base + "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=TIMEOUT) as response:
        if response.status != 200:
            raise RuntimeError(f"Source returned HTTP {response.status}")
        return json.load(response)

def github_repositories(query: str, limit: int = 5) -> list[dict]:
    """Find public GitHub repos using official search API (rate-limited unauthenticated)."""
    if not 2 <= len(query.strip()) <= 160:
        raise ValueError("Search query must contain 2-160 characters")
    data = _json_get("https://api.github.com/search/repositories",
                     {"q": query, "sort": "stars", "order": "desc", "per_page": min(max(limit, 1), 10)})
    return [{"name": x.get("full_name"), "url": x.get("html_url"),
             "description": x.get("description"), "stars": x.get("stargazers_count"),
             "license": (x.get("license") or {}).get("spdx_id"), "source": "github"}
            for x in data.get("items", [])]

def research_papers(query: str, limit: int = 5) -> list[dict]:
    """Search OpenAlex public metadata for research papers."""
    if not 2 <= len(query.strip()) <= 160:
        raise ValueError("Search query must contain 2-160 characters")
    data = _json_get("https://api.openalex.org/works",
                     {"search": query, "per-page": min(max(limit, 1), 10)})
    return [{"title": x.get("display_name"), "url": x.get("doi") or x.get("id"),
             "year": x.get("publication_year"), "source": "openalex"}
            for x in data.get("results", [])]

def discover(query: str) -> dict:
    """Return evidence and source errors separately; never claim a failed search succeeded."""
    output = {"query": query, "results": [], "errors": []}
    for name, fn in (("github", github_repositories), ("openalex", research_papers)):
        try:
            output["results"].extend(fn(query))
        except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError, OSError) as exc:
            output["errors"].append({"source": name, "error": str(exc)})
    return output
