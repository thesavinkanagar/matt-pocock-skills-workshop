# 03: Anonymous heart click goes to sign in

**What to build:** An anonymous shopper sees the heart on catalog cards, but clicking it takes them to the sign-in page. After signing in they return to the same catalog page they were on (same filters and page), with nothing saved; they click the heart again to save it. There are no anonymous Favourites. See `.scratch/favourites/spec.md`.

**Blocked by:** 01 (Save a Favourite and see it on the Favourites page)

**Status:** ready-for-agent

- [x] Anonymous catalog cards show an empty heart
- [x] Clicking it navigates to sign in with the current catalog URL as the return-to
- [x] After signing in, the shopper lands back on that catalog page and no Favourite has been saved
- [x] While anonymous, the catalog makes no calls to the favourites API
- [x] Backend test confirms anonymous and basket-id-only requests can't create Favourites (401); the redirect flow is checked by hand in the browser

## Comments

- Implemented: anonymous catalog cards show an empty heart; clicking it goes to sign in with the current catalog URL (path and query) as the return-to, and the catalog makes no favourites calls while anonymous. Backend test `test_anonymous_heart_click_saves_nothing_after_signing_in` guards that nothing is saved; redirect flow checked by hand in the browser.
