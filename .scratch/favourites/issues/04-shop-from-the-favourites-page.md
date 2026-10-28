# 04: Shop from the Favourites page

**What to build:** The Favourites page becomes somewhere to shop from. Each Favourite shows its current price and an "Add to basket" button that behaves exactly as it does in the catalog. Adding to the basket or checking out leaves the Favourite in place. With no Favourites the page shows a short message and a link back to the catalog, and a Favourite whose Product no longer exists is left out silently. See `.scratch/favourites/spec.md`.

**Blocked by:** 01 (Save a Favourite and see it on the Favourites page)

**Status:** ready-for-agent

- [ ] Each card on the Favourites page has an "Add to basket" button with the same behaviour as the catalog card
- [ ] `GET /api/favourites` shows the Product's current price
- [ ] Adding a Favourite to the basket and placing an order leaves it in `GET /api/favourites`
- [ ] A Favourite whose Product no longer exists is omitted from `GET /api/favourites` without an error
- [ ] With no Favourites, the page shows a short message and a link to the catalog
- [ ] Backend tests through the HTTP API with the `client` fixture cover the above; frontend checked by hand in the browser
