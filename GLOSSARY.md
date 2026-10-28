# eShop

A small online store where shoppers browse a catalog, fill a basket and place orders.

## Language

### People and products

**Shopper**:
A person using the store. A shopper is either signed in (known by their email) or anonymous.
_Avoid_: Buyer, user, customer

**Product**:
Something for sale in the catalog, with a name, description, price, brand and type.
_Avoid_: Catalog item, item

### Favourites

**Favourite**:
A product a signed-in shopper has marked to come back to later. It is independent of the basket: adding a Favourite to the basket or ordering it does not remove it.
_Avoid_: Wishlist, saved item, bookmark, favorite (US spelling)

**Favourites page**:
The one place a signed-in shopper sees all their Favourites, newest first.
_Avoid_: Wishlist page, saved list
