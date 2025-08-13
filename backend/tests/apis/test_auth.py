def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test_new@example.com",
            "password": "password",
            "username": "testuser_new",
            "full_name": "Test User New",
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "test_new@example.com"
    assert data["username"] == "testuser_new"
    assert data["full_name"] == "Test User New"
    assert data["is_active"] is True
    assert "id" in data

    assert "password" not in data
    assert "password_hash" not in data


def test_register_existing_user(client):
    client.post(
        "/auth/register",
        json={
            "email": "test_existing@example.com",
            "password": "password",
            "username": "testuser_existing",
            "full_name": "Test User Existing",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "email": "test_existing@example.com",
            "password": "password",
            "username": "testuser_existing",
            "full_name": "Test User Existing",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email já registrado"}


def test_login_for_access_token(client):
    client.post(
        "/auth/register",
        json={"email": "test_login@example.com", "password": "password", "username": "testuser_login", "full_name": "Test User Login"},
    )
    response = client.post(
        "/auth/token",
        data={"username": "test_login@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client):
    client.post(
        "/auth/register",
        json={"email": "test_me@example.com", "password": "password", "username": "testuser_me", "full_name": "Test User Me"},
    )
    response = client.post(
        "/auth/token",
        data={"username": "test_me@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_me@example.com"
    assert data["username"] == "testuser_me"
