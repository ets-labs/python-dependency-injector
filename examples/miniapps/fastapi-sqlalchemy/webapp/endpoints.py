"""Endpoints module."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from dependency_injector.wiring import Provide, inject

from .containers import Container
from .repositories import NotFoundError
from .services import UserService

router = APIRouter()


@router.get("/users")
@inject
def get_list(
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
):
    return user_service.get_users()


@router.get("/users/{user_id}")
@inject
def get_by_id(
    user_id: int,
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
):
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/users", status_code=status.HTTP_201_CREATED)
@inject
def add(
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
):
    return user_service.create_user()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
    user_id: int,
    user_service: Annotated[UserService, Depends(Provide[Container.user_service])],
) -> Response:
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/status")
def get_status():
    return {"status": "OK"}
