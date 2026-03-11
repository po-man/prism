from typing import Any, Dict, List, Optional
from pydantic import BaseModel, AnyHttpUrl, Field


class WebSearchResult(BaseModel):
    """A model for a single item in the web_search_results context array."""

    original_text: str
    url: AnyHttpUrl


class ProvenanceContext(BaseModel):
    """
    Contextual information required to resolve provenance, including base URLs
    for reports and the original web search results.
    """

    attached_reports: List[AnyHttpUrl] = Field(default_factory=list)
    web_search_results: List[WebSearchResult] = Field(default_factory=list)


class ProvenanceRequest(BaseModel):
    """
    The request payload for the /resolve-provenance endpoint, containing the
    data blob to be processed and the necessary context.
    """

    data: List[Dict[str, Any]]
    context: ProvenanceContext