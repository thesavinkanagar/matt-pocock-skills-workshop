from db.client import DatabaseClient
from models.schemas import CatalogItemResponse
from services.catalog_service import to_product_response


class ProductNotFoundError(ValueError):
    pass


class FavouritesService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def list_for_shopper(self, email: str) -> list[CatalogItemResponse]:
        return [to_product_response(item) for item in self.db.list_favourite_products(email)]

    def add(self, email: str, product_id: int) -> None:
        if self.db.get_catalog_item_by_id(product_id) is None:
            raise ProductNotFoundError("Product not found")
        self.db.add_favourite(email, product_id)

    def remove(self, email: str, product_id: int) -> None:
        """Removing something that isn't a Favourite succeeds quietly."""
        self.db.remove_favourite(email, product_id)
