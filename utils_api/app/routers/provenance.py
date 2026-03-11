import httpx
import asyncio
from urllib.parse import quote as url_quote
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import AnyHttpUrl

from app.schemas.provenance import ProvenanceContext, ProvenanceRequest

router = APIRouter()


async def _resolve_redirect(url: AnyHttpUrl, client: httpx.AsyncClient) -> AnyHttpUrl:
    """Follows a redirect to find the final URL."""
    try:
        response = await client.head(str(url), follow_redirects=True, timeout=10.0)
        response.raise_for_status()
        return response.url
    except httpx.RequestError as e:
        # If resolution fails, return the original URL but it might not work.
        # Consider logging this event.
        return url


def _find_and_resolve_sources(
    data: Union[Dict, List], context: ProvenanceContext, web_search_urls: Dict[int, AnyHttpUrl]
) -> None:
    """Recursively traverses the data to find and resolve 'source' objects."""
    if isinstance(data, dict):
        if "source_type" in data and "resolved_url" in data:
            source = data
            source_type = source.get("source_type")
            page_number = source.get("page_number")
            search_index = source.get("search_result_index")
            quote = source.get("quote")

            if source_type in ["annual_report", "financial_report"] and page_number:
                base_url = (
                    context.annual_report_url
                    if source_type == "annual_report"
                    else context.financial_report_url
                )
                if base_url:
                    source["resolved_url"] = f"{base_url}#page={page_number}"

            elif source_type == "web_search" and search_index is not None and quote:
                if search_index in web_search_urls:
                    base_url = web_search_urls[search_index]
                    encoded_quote = url_quote(quote)
                    source["resolved_url"] = f"{base_url}#:~:text={encoded_quote}"

        for key, value in data.items():
            _find_and_resolve_sources(value, context, web_search_urls)

    elif isinstance(data, list):
        for item in data:
            _find_and_resolve_sources(item, context, web_search_urls)


@router.post(
    "/resolve-provenance",
    tags=["Utilities"],
    summary="Resolves provenance URLs for impact and financial data.",
)
async def resolve_provenance(payload: ProvenanceRequest = Body(...)):
    """
    Recursively finds all `source` objects within a nested dictionary and
    populates the `resolved_url` field by combining contextual base URLs with
    page numbers or text fragments. It also resolves any redirecting URLs for
    web sources.
    """
#    async with httpx.AsyncClient() as client:
#        tasks = {
#            i: _resolve_redirect(result.url, client)
#            for i, result in enumerate(payload.context.web_search_results)
#        }
#        resolved_urls = await asyncio.gather(*tasks.values())
    web_search_urls = {index: url for index, url in enumerate(payload.context.web_search_results)}

    _find_and_resolve_sources(payload.data, payload.context, web_search_urls)
    return dict(data=payload.data)