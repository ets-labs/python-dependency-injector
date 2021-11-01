"""Endpoints module."""

from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


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
        query: Optional[str] = None,
        limit: Optional[str] = None,
        default_query: str = Depends(Provide[Container.config.default.query]),
        default_limit: int = Depends(Provide[Container.config.default.limit.as_int()]),
        search_service: SearchService = Depends(Provide[Container.search_service]),
):
    query = query or default_query
    limit = limit or default_limit

    gifs = await search_service.search(query, limit)

    return {
        "query": query,
        "limit": limit,
        "gifs": gifs,
    }
