# 04: Shop from the Favourites page

**What to build:** The Favourites page becomes somewhere to shop from. Each Favourite shows its current price and an "Add to basket" button that behaves exactly as it does in the catalog. Adding to the basket or checking out leaves the Favourite in place. With no Favourites the page shows a short message and a link back to the catalog, and a Favourite whose Product no longer exists is left out silently. See `.scratch/favourites/spec.md`.

**Blocked by:** 01 (Save a Favourite and see it on the Favourites page)

**Status:** ready-for-agent

- [x] Each card on the Favourites page has an "Add to basket" button with the same behaviour as the catalog card
- [x] `GET /api/favourites` shows the Product's current price
- [x] Adding a Favourite to the basket and placing an order leaves it in `GET /api/favourites`
- [x] A Favourite whose Product no longer exists is omitted from `GET /api/favourites` without an error
- [x] With no Favourites, the page shows a short message and a link to the catalog
- [x] Backend tests through the HTTP API with the `client` fixture cover the above; frontend checked by hand in the browser

## Comments

- Implemented: empty state on the Favourites page with a link to the catalog. Add to basket, current price and skipping missing Products already worked via the shared product card and the live join; new tests in `python-eshop/backend/tests/test_favourites.py` guard the price, checkout and missing-Product cases. Frontend checked by hand in the browser.
