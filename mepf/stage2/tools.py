"""Retrieval tools used by the planning agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class RetrievalToolbox:
    """Tool facade for keyword search, reverse image search, and evidence lookup."""

    def __init__(self, config: dict) -> None:
        self.config = config

    def keyword_search(self, query: str) -> list[SearchResult]:
        # TODO: Connect to Google Search API / SerpAPI from `3_news`.
        return [
            SearchResult(
                title="placeholder evidence",
                url="https://example.com",
                snippet=f"Evidence placeholder for query: {query}",
            )
        ]

    def reverse_image_search(self, image_path: str) -> list[SearchResult]:
        # TODO: Connect to reverse image search used in retrieval notebooks.
        return [
            SearchResult(
                title="placeholder image provenance",
                url="https://example.com/image",
                snippet=f"Image provenance placeholder for: {image_path}",
            )
        ]
