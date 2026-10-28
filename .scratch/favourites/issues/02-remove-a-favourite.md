# 02: Remove a Favourite

**What to build:** A signed-in shopper can remove a Favourite either by clicking its filled heart in the catalog or by clicking a remove button on its card on the Favourites page. Removing something that's already gone succeeds quietly, so stale tabs never show an error. See `.scratch/favourites/spec.md`.

**Blocked by:** 01 (Save a Favourite and see it on the Favourites page)

**Status:** ready-for-agent

- [x] `DELETE /api/favourites/{product_id}` removes the Favourite; it no longer appears in `GET /api/favourites`
- [x] Removing a Product that isn't a Favourite also succeeds
- [x] `DELETE` returns 401 with no credentials and with only an `X-Basket-Id` header
- [x] One shopper removing a Product never affects another shopper's Favourites
- [x] Clicking a filled heart in the catalog removes the Favourite and empties the heart
- [x] Each card on the Favourites page has a remove button that removes it from the page
- [x] Backend tests through the HTTP API with the `client` fixture cover the above; frontend checked by hand in the browser

## Comments

- Implemented: `DELETE /api/favourites/{product_id}` (idempotent, sign-in only), filled catalog heart now removes, and each Favourites page card has a Remove button. Backend tests in `python-eshop/backend/tests/test_favourites.py`; frontend checked by hand in the browser.
