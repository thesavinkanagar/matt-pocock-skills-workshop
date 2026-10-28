import sqlite3

from config import settings
from tests.conftest import login


def favourite_ids(client, headers):
    response = client.get("/api/favourites", headers=headers)
    assert response.status_code == 200, response.text
    return [product["id"] for product in response.json()]


def save(client, headers, product_id):
    response = client.put(f"/api/favourites/{product_id}", headers=headers)
    assert response.status_code == 200, response.text
    return response


def register(client, email):
    response = client.post(
        "/api/auth/register", json={"email": email, "password": "secret123"}
    )
    assert response.status_code == 200, response.text
    return login(client, email=email, password="secret123")


def test_saved_favourite_is_listed_as_a_catalog_product(client, demo_headers):
    save(client, demo_headers, 3)

    favourites = client.get("/api/favourites", headers=demo_headers).json()

    catalog = client.get("/api/catalog/items").json()["items"]
    product = next(item for item in catalog if item["id"] == 3)
    assert favourites == [product]


def test_favourites_are_listed_newest_first(client, demo_headers):
    for product_id in [2, 7, 5]:
        save(client, demo_headers, product_id)

    assert favourite_ids(client, demo_headers) == [5, 7, 2]


def test_saving_twice_keeps_one_favourite_in_its_original_position(
    client, demo_headers
):
    for product_id in [2, 7, 5]:
        save(client, demo_headers, product_id)

    save(client, demo_headers, 7)

    assert favourite_ids(client, demo_headers) == [5, 7, 2]


def test_saving_an_unknown_product_is_not_found(client, demo_headers):
    response = client.put("/api/favourites/99999", headers=demo_headers)

    assert response.status_code == 404
    assert favourite_ids(client, demo_headers) == []


def test_anonymous_shoppers_cannot_list_or_save_favourites(client, anon_headers):
    for headers in [{}, anon_headers]:
        listed = client.get("/api/favourites", headers=headers)
        saved = client.put("/api/favourites/1", headers=headers)

        assert listed.status_code == 401
        assert saved.status_code == 401
        assert listed.json()["detail"] == "Authentication required"


def test_shoppers_favourites_are_isolated(client, demo_headers):
    other = register(client, "other@example.com")

    save(client, demo_headers, 1)
    save(client, other, 4)

    assert favourite_ids(client, demo_headers) == [1]
    assert favourite_ids(client, other) == [4]


def remove(client, headers, product_id):
    response = client.delete(f"/api/favourites/{product_id}", headers=headers)
    assert response.status_code == 200, response.text
    return response


def test_removed_favourite_is_no_longer_listed(client, demo_headers):
    for product_id in [2, 7, 5]:
        save(client, demo_headers, product_id)

    remove(client, demo_headers, 7)

    assert favourite_ids(client, demo_headers) == [5, 2]


def test_removing_a_product_that_is_not_a_favourite_succeeds(client, demo_headers):
    save(client, demo_headers, 2)

    remove(client, demo_headers, 9)
    remove(client, demo_headers, 99999)

    assert favourite_ids(client, demo_headers) == [2]


def test_anonymous_shoppers_cannot_remove_favourites(client, demo_headers, anon_headers):
    save(client, demo_headers, 1)

    for headers in [{}, anon_headers]:
        response = client.delete("/api/favourites/1", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Authentication required"

    assert favourite_ids(client, demo_headers) == [1]


def test_removing_never_touches_another_shoppers_favourites(client, demo_headers):
    other = register(client, "other@example.com")
    save(client, demo_headers, 3)
    save(client, other, 3)

    remove(client, other, 3)

    assert favourite_ids(client, demo_headers) == [3]
    assert favourite_ids(client, other) == []


def test_anonymous_heart_click_saves_nothing_after_signing_in(client, anon_headers):
    attempt = client.put("/api/favourites/3", headers=anon_headers)
    assert attempt.status_code == 401

    headers = login(client, headers=anon_headers)

    assert favourite_ids(client, headers) == []


def test_favourites_show_the_current_price(client, demo_headers):
    save(client, demo_headers, 3)
    with sqlite3.connect(settings.database_path) as conn:
        conn.execute("UPDATE catalog_items SET price = 42.5 WHERE id = 3")

    favourites = client.get("/api/favourites", headers=demo_headers).json()

    assert favourites[0]["price"] == 42.5


def test_buying_a_favourite_keeps_it_a_favourite(client, demo_headers):
    save(client, demo_headers, 3)

    basket = client.post(
        "/api/basket/items", json={"catalog_item_id": 3}, headers=demo_headers
    ).json()
    order = client.post(
        "/api/orders", json={"basket_id": basket["id"]}, headers=demo_headers
    )
    assert order.status_code == 200, order.text

    assert favourite_ids(client, demo_headers) == [3]


def test_favourite_whose_product_no_longer_exists_is_left_out(client, demo_headers):
    for product_id in [2, 3]:
        save(client, demo_headers, product_id)
    with sqlite3.connect(settings.database_path) as conn:
        conn.execute("DELETE FROM catalog_items WHERE id = 2")

    assert favourite_ids(client, demo_headers) == [3]
