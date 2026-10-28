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
