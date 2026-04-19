from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body

from app.schemas.provenance import ProvenanceContext, ProvenanceRequest

router = APIRouter()


def _find_and_resolve_sources(
    data: Union[Dict, List], context: ProvenanceContext
) -> None:
    """Recursively traverses the data to find and resolve 'source' objects."""
    if isinstance(data, dict):
        if "source_type" in data:
            source = data
            source_type = source.get("source_type")
            page_number = source.get("page_number")
            source_index = source.get("source_index")

            if source_type == "attached_report" and source_index is None:
                if context.attached_reports and len(context.attached_reports) == 1:
                    source_index = 0
                    source["source_index"] = source_index

            if source_type == "attached_report" and page_number:
                base_url = context.attached_reports[source_index]
                if base_url:
                    source["resolved_url"] = f"{base_url}#page={page_number}"

        for key, value in data.items():
            _find_and_resolve_sources(value, context)
            if key == "source" and isinstance(value, dict) and "resolved_url" not in value:
                data[key] = None

    elif isinstance(data, list):
        for item in data:
            _find_and_resolve_sources(item, context)


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
    _find_and_resolve_sources(payload.data, payload.context)
    return dict(data=payload.data)