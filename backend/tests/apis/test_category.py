# from fastapi.testclient import TestClient

# from app.main import app

# client = TestClient(app)


# def test_create_category():
#     response = client.post("/categories/", json={"name": "Test Category"})
#     assert response.status_code == 201
#     data = response.json()
#     assert data["name"] == "Test Category"
#     assert "id" in data


# def test_get_categories():
#     response = client.get("/categories/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_update_category():
#     response = client.post("/categories/", json={"name": "Test Category for Update"})
#     category_id = response.json()["id"]
#     response = client.put(
#         f"/categories/{category_id}", json={"name": "Updated Category"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Updated Category"


# def test_delete_category():
#     response = client.post("/categories/", json={"name": "Test Category for Delete", "description": "A test category for delete", "icon": "test_icon_delete"})
#     category_id = response.json()["id"]
#     response = client.delete(f"/categories/{category_id}")
#     assert response.status_code == 204
