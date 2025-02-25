"""Endpoints module."""

from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependency_injector.wiring import Provide, inject

from .containers import Container
from .services import SearchService


class Gif(BaseModel):
    url: str


class Response(BaseModel):
    query: str
    limit: int
    gifs: List[Gif]


router = APIRouter()


@router.get("/", response_model=Response)
@inject
async def index(
    default_query: Annotated[str, Depends(Provide[Container.config.default.query])],
    default_limit: Annotated[
        int, Depends(Provide[Container.config.default.limit.as_int()])
    ],
    search_service: Annotated[
        SearchService, Depends(Provide[Container.search_service])
    ],
    query: str | None = None,
    limit: int | None = None,
):
    query = query or default_query
    limit = limit or default_limit

    gifs = await search_service.search(query, limit)

    return {
        "query": query,
        "limit": limit,
        "gifs": gifs,
    }
