import httpx
import asyncio
from fastapi import APIRouter, Body
from pydantic import AnyHttpUrl

from app.schemas.url_resolver import UrlResolverRequest, UrlResolverItem, UrlResolverResponse

router = APIRouter()


@router.post(
    "/resolve-search-urls",
    response_model=UrlResolverResponse,
    tags=["Utilities"],
)
async def resolve_search_urls(payload: UrlResolverRequest = Body(...)):
    """
    Resolves redirecting URLs (like 301, 302) to their final destination.

    - **Input**: A list of objects, each with `original_text` and a `url`.
    - **Output**: The same list, with URLs updated to their final destination if they were redirected.
    """

    async def resolve_url(item: UrlResolverItem, client: httpx.AsyncClient) -> UrlResolverItem:
        try:
            response = await client.head(str(item.url), follow_redirects=False, timeout=10.0)
            if response.status_code == 404:
                return None
            if response.is_redirect:
                redirect_url = response.headers.get("location")
                if redirect_url:
                    # Resolve the redirect URL, which might be relative
                    item.url = AnyHttpUrl(str(response.url.join(redirect_url)))
        except httpx.RequestError:
            return None
        return item

    async with httpx.AsyncClient() as client:
        tasks = [resolve_url(item, client) for item in payload.search_results]
        results = await asyncio.gather(*tasks)
        # Convert model instances back to dictionaries for response model validation
        result_dicts = [item.model_dump() for item in results if item is not None]
        return UrlResolverResponse(search_results=result_dicts)
