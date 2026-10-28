from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_favourites_service, require_authenticated_user
from models.schemas import CatalogItemResponse
from services.favourites_service import FavouritesService, ProductNotFoundError

router = APIRouter(prefix="/api/favourites", tags=["favourites"])


@router.get("", response_model=list[CatalogItemResponse])
def list_favourites(
    email: str = Depends(require_authenticated_user),
    service: FavouritesService = Depends(get_favourites_service),
):
    return service.list_for_shopper(email)


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def add_favourite(
    product_id: int,
    email: str = Depends(require_authenticated_user),
    service: FavouritesService = Depends(get_favourites_service),
):
    try:
        service.add(email, product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return {"product_id": product_id, "favourite": True}
