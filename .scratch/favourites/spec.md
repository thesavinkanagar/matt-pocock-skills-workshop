# Spec: Favourites

Status: ready-for-agent

## Problem Statement

A signed-in shopper browsing the catalog sees products they like but aren't ready to buy. Today the only way to keep track of them is to put them in the basket, which mixes "maybe later" with "buying now", or to remember them. There's no place to come back to the Products they were interested in.

## Solution

Signed-in shoppers can mark any Product as a Favourite by clicking a heart on its card in the catalog, and unmark it by clicking again. A Favourites page, linked from the header, lists all their Favourites, newest first, as ordinary product cards with the current price, an "Add to basket" button and a remove button. Favourites belong to the shopper's account, so they're there whenever they sign in. Anonymous shoppers who click a heart are sent to sign in first.

## User Stories

1. As a signed-in shopper, I want to click a heart on a product card, so that I can save that Product as a Favourite without leaving the catalog.
2. As a signed-in shopper, I want the heart to appear filled on Products that are already Favourites, so that I can tell at a glance what I've saved.
3. As a signed-in shopper, I want to click a filled heart to remove that Favourite, so that I can change my mind from the catalog.
4. As a signed-in shopper, I want a "Favourites" link in the header, so that I can reach my Favourites page from anywhere.
5. As a signed-in shopper, I want the Favourites page to list my Favourites newest first, so that what I saved most recently is at the top.
6. As a signed-in shopper, I want each Favourite shown as a normal product card with its current price, so that I see what it costs today, not when I saved it.
7. As a signed-in shopper, I want an "Add to basket" button on each Favourite, so that I can buy something I saved without going back to the catalog.
8. As a signed-in shopper, I want "Add to basket" on the Favourites page to behave exactly as it does in the catalog, so that the store feels consistent.
9. As a signed-in shopper, I want a Favourite to stay a Favourite after I add it to my basket or order it, so that I can buy it again later.
10. As a signed-in shopper, I want a remove button on each card on the Favourites page, so that I can tidy my list in place.
11. As a signed-in shopper, I want a short message and a link to the catalog when I have no Favourites, so that an empty page doesn't look broken.
12. As a signed-in shopper, I want saving the same Product twice (e.g. from two tabs) to leave a single Favourite and show no error, so that double clicks are harmless.
13. As a signed-in shopper, I want removing something that's already gone to succeed quietly, so that stale tabs don't show errors.
14. As a signed-in shopper, I want my Favourites to be there next time I sign in, on any device, so that they're tied to me, not this browser.
15. As a signed-in shopper, I want no limit on how many Favourites I can keep, so that I never have to choose what to drop.
16. As a signed-in shopper, I want a Favourite whose Product no longer exists to be left out of my Favourites page silently, so that the page never shows broken cards.
17. As an anonymous shopper, I want clicking a heart to take me to sign in and then back to the catalog page I was on, so that I don't lose my place.
18. As an anonymous shopper, I don't expect anything to be saved until I've signed in and clicked the heart again, so that the behaviour is predictable.
19. As an anonymous shopper, I want the Favourites link hidden from the header, so that I'm not shown a page I can't use.
20. As an anonymous shopper visiting the Favourites page directly, I want to be sent to sign in and then returned to the Favourites page, matching how the Orders page works.
21. As a signed-in shopper, I want nobody else, signed in or anonymous, to be able to see or change my Favourites, so that my list stays mine.

## Implementation Decisions

- **Layering** follows the repo convention: a new favourites router for HTTP concerns, a new favourites service for rules, and new SQL methods on the existing database client. No new framework or dependency.
- **Schema:** a new `favourites` table with the shopper's email, the product id, and the time it was added (timezone-aware UTC, stored like order dates). One row per (email, product) pair, enforced by a unique constraint so saving twice is a no-op.
- **Identity:** every favourites endpoint requires a signed-in shopper, using the existing "require authenticated user" dependency. A request with only an anonymous basket id (`X-Basket-Id`) is refused with 401. It never reads or writes anyone's Favourites. There are no anonymous Favourites, and Favourites are not merged at sign-in.
- **API contract** (all under `/api/favourites`, bearer token required):
  - `GET /api/favourites` returns the shopper's Favourites as a list of product objects in the same shape the catalog returns, newest first. Ties on the added time fall back to insertion order, so the order stays the same between requests. Favourites whose Product no longer exists are left out.
  - `PUT /api/favourites/{product_id}` adds a Favourite. It's idempotent: saving an existing Favourite succeeds and doesn't change its added time. An unknown product id returns 404.
  - `DELETE /api/favourites/{product_id}` removes a Favourite. It's idempotent: removing one that doesn't exist also succeeds.
  - Anonymous calls return 401 with the same message as other sign-in-only endpoints.
- **Catalog hearts:** when signed in, the catalog page fetches the shopper's Favourites once and fills in hearts from that list. When anonymous it doesn't call the favourites API at all, and clicking a heart sends the shopper to the login page with a return-to of the current catalog URL. The heart is a button with an accessible label ("Add to Favourites" / "Remove from Favourites").
- **Favourites page:** a new `/favourites` route reusing the existing product card plus a remove control. It redirects anonymous visitors to login with return-to `/favourites`, as the Orders page does.
- **Header:** a "Favourites" link shown only when signed in, with no count badge.
- **Frontend API client** gains functions to list, add and remove Favourites, using the same auth header handling as existing calls.
- **Basket and orders are untouched:** adding a Favourite to the basket or placing an order never changes Favourites.

## Testing Decisions

- **One seam: the HTTP API.** All behaviour is tested through the favourites endpoints with the existing `client` fixture (in-process API against a throwaway database) and the `login` helper / `demo_headers` / `anon_headers` fixtures.
- Good tests exercise external behaviour only: status codes and response bodies from real requests. They don't call the service or database client directly or inspect table rows.
- Cases to cover:
  - Add then list returns the Product. List is newest first across several adds.
  - Adding twice leaves a single Favourite and keeps the original position.
  - Removing works, and removing a missing Favourite still succeeds.
  - Unknown product id on add returns 404.
  - Anonymous (no headers, and `X-Basket-Id` only) gets 401 on list, add and remove.
  - Two shoppers' Favourites are isolated (register a second shopper and check neither sees or changes the other's).
  - Adding a Favourite to the basket and checking out leaves it in Favourites.
  - The list shows the current product price.
- **Prior art:** the basket identity tests (shopper isolation, anonymous-vs-signed-in refusal), checkout tests, and order timestamp tests (UTC times).
- **Frontend** has no test setup and none is added. The heart, header link, Favourites page, empty state and sign-in redirects are checked by hand in the browser.

## Out of Scope

- Anonymous Favourites, and merging Favourites at sign-in.
- Automatically saving the Favourite after an anonymous shopper signs in from a heart click.
- A heart anywhere other than catalog product cards (there's no product detail page).
- Count badges, pagination, sorting or filtering on the Favourites page, and any limit on the number of Favourites.
- Price-change or back-in-stock notifications.
- Renaming existing code (`buyer`, `CatalogItem`) to match the glossary.
- Admin features, and deleting Products (nothing deletes Products today; skipping missing ones is only a safety net).

## Further Notes

- Vocabulary follows `GLOSSARY.md`: Shopper, Product, Favourite, Favourites page. Use Australian spelling ("favourite") in UI copy, API paths and code.
- No ADRs were recorded for this feature; none of the decisions is hard to reverse.
