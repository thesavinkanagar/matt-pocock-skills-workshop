# 01: Save a Favourite and see it on the Favourites page

**What to build:** A signed-in shopper clicks a heart on a product card in the catalog; the heart fills and the Product appears on a new Favourites page, newest first, reached from a "Favourites" header link that only signed-in shoppers see. Favourites belong to the shopper's account and nobody else can see them. This is the tracer bullet: storage, the add and list endpoints, the heart and the page, end to end. See `.scratch/favourites/spec.md`.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] Favourites are stored per signed-in shopper with the time added (timezone-aware UTC), one per shopper and Product
- [x] `PUT /api/favourites/{product_id}` saves a Favourite; saving an existing one succeeds and keeps its original position
- [x] `PUT` with an unknown product id returns 404
- [x] `GET /api/favourites` returns the shopper's Favourites as product objects in the catalog's shape, newest first, with a stable order on ties
- [x] Both endpoints return 401 with no credentials and with only an `X-Basket-Id` header
- [x] Two shoppers' Favourites are isolated: one shopper's saves never appear for the other
- [x] Signed-in catalog cards show a heart that is filled for existing Favourites; clicking an empty heart saves it and fills it
- [x] The heart is a button with an accessible label ("Add to Favourites" / "Remove from Favourites")
- [x] A "Favourites" header link appears only when signed in, with no count
- [x] `/favourites` lists the Favourites as product cards; an anonymous visit redirects to sign in and returns to `/favourites`
- [x] Backend tests through the HTTP API with the `client` fixture cover the above; frontend checked by hand in the browser

## Comments

- Implemented: `favourites` table, `PUT`/`GET /api/favourites`, catalog heart (signed-in only), header link and `/favourites` page. Backend tests in `python-eshop/backend/tests/test_favourites.py`; frontend checked by hand in the browser. A filled heart is shown but disabled until 02 adds removing.
