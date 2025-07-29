from datetime import datetime


def test_create_warning(client, admin_token):
    response_category = client.post(
        "/category/",
        json={
            "name": "Test Category for Warning",
            "description": "Description Test Category",
            "icon": "mdi-test",
        },
        headers={"Authorization": admin_token},
    )
    category_id = response_category.json()["id"]
    response = client.post(
        "/warnings/",
        json={
            "title": "Test Warning",
            "event_date": "2025-01-01T12:00:00",
            "content": "Test Warning",
            "category_id": category_id,
        },
        headers={"Authorization": admin_token},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Warning"
    assert data["content"] == "Test Warning"
    assert "id" in data


def test_get_warnings(client):
    response = client.get("/warnings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_warning(client, admin_token):
    # First, create a category and a warning to update
    response_category = client.post(
        "/category/",
        json={
            "name": "Test Category for Warning Update",
            "description": "Description Test Category Update",
            "icon": "mdi-test-update",
        },
        headers={"Authorization": admin_token},
    )
    category_id = response_category.json()["id"]

    response = client.post(
        "/warnings/",
        json={
            "title": "Test Warning for Update",
            "event_date": datetime.now().isoformat(),
            "content": "Test Warning for Update",
            "category_id": category_id,
        },
        headers={"Authorization": admin_token},
    )
    warning_id = response.json()["id"]

    response = client.put(
        f"/warnings/{warning_id}",
        json={"content": "Updated Warning"},
        headers={"Authorization": admin_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated Warning"
    assert data["title"] == "Test Warning for Update"


def test_delete_warning(client, admin_token):
    # First, create a category and a warning to delete
    response_category = client.post(
        "/category/",
        json={
            "name": "Test Category for Warning Delete",
            "description": "Description Test Category Delete",
            "icon": "mdi-test-delete",
        },
        headers={"Authorization": admin_token},
    )
    category_id = response_category.json()["id"]
    
    response = client.post(
        "/warnings/",
        json={
            "title": "Test Warning for Delete",
            "event_date": datetime.now().isoformat(),
            "content": "This is a test warning for delete.",
            "category_id": category_id,
        },
        headers={"Authorization": admin_token},
    )
    warning_id = response.json()["id"]

    response = client.delete(
        f"/warnings/{warning_id}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 204
