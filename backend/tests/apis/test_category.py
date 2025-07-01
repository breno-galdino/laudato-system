def test_create_category(client):
    response = client.post("/category/", json={"name": "Test Category", "description": "A test category", "icon": "test_icon"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "A test category"
    assert data["icon"] == "test_icon"
    assert "id" in data


def test_get_categories(client):
    response = client.get("/category/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_category(client):
    response = client.post("/category/", json={"name": "Test Category for Update", "description": "A test category for update", "icon": "test_icon_update"})
    category_id = response.json()["id"]
    response = client.put(
        f"/category/{category_id}", json={"name": "Updated Category"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["description"] == "A test category for update"


def test_delete_category(client):
    response = client.post("/category/", json={"name": "Test Category for Delete", "description": "A test category for delete", "icon": "test_icon_delete"})
    category_id = response.json()["id"]
    response = client.delete(f"/category/{category_id}")
    assert response.status_code == 204
