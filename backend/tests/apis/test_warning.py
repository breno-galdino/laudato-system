# from fastapi.testclient import TestClient

# from app.main import app

# client = TestClient(app)


# def test_create_warning():
#     # First, create a category to associate with the warning
#     response = client.post("/categories/", json={"name": "Test Category for Warning"})
#     category_id = response.json()["id"]

#     response = client.post(
#         "/warnings/",
#         json={
#             "message": "Test Warning",
#             "category_id": category_id,
#             "published": True,
#             "user_id": 1,
#         },
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["message"] == "Test Warning"
#     assert "id" in data


# def test_get_warnings():
#     response = client.get("/warnings/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_update_warning():
#     # First, create a category and a warning to update
#     response = client.post("/categories/", json={"name": "Test Category for Warning Update"})
#     category_id = response.json()["id"]
#     response = client.post(
#         "/warnings/",
#         json={
#             "message": "Test Warning for Update",
#             "category_id": category_id,
#             "published": True,
#             "user_id": 1,
#         },
#     )
#     warning_id = response.json()["id"]

#     response = client.put(
#         f"/warnings/{warning_id}", json={"message": "Updated Warning"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "Updated Warning"


# def test_delete_warning():
#     # First, create a category and a warning to delete
#     response = client.post("/categories/", json={"name": "Test Category for Warning Delete"})
#     category_id = response.json()["id"]
#     response = client.post(
#         "/warnings/",
#         json={
#             "title": "Test Warning for Delete",
#             "event_date": "2025-01-01T12:00:00",
#             "content": "This is a test warning for delete.",
#             "category_id": category_id,
#         },
#     )
#     warning_id = response.json()["id"]

#     response = client.delete(f"/warnings/{warning_id}")
#     assert response.status_code == 204
