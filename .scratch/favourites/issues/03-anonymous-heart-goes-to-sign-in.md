# 03: Anonymous heart click goes to sign in

**What to build:** An anonymous shopper sees the heart on catalog cards, but clicking it takes them to the sign-in page. After signing in they return to the same catalog page they were on (same filters and page), with nothing saved; they click the heart again to save it. There are no anonymous Favourites. See `.scratch/favourites/spec.md`.

**Blocked by:** 01 (Save a Favourite and see it on the Favourites page)

**Status:** ready-for-agent

- [ ] Anonymous catalog cards show an empty heart
- [ ] Clicking it navigates to sign in with the current catalog URL as the return-to
- [ ] After signing in, the shopper lands back on that catalog page and no Favourite has been saved
- [ ] While anonymous, the catalog makes no calls to the favourites API
- [ ] Backend test confirms anonymous and basket-id-only requests can't create Favourites (401); the redirect flow is checked by hand in the browser
