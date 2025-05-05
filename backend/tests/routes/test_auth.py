HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401


def test_register_route(client, init_database):
    user_data = {
        "email": "routeuser@example.com",
        "username": "routeuser",
        "password": "Password123!",
    }

    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == HTTP_CREATED
    data = response.json
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_register_duplicate_email_route(client, init_database):
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "Password123!",
    }
    client.post("/api/auth/register", json=user_data)

    duplicate_data = {
        "email": "duplicate@example.com",
        "username": "user2",
        "password": "Password123!",
    }

    response = client.post("/api/auth/register", json=duplicate_data)
    assert response.status_code == HTTP_BAD_REQUEST
    assert "error" in response.json
    assert "Email already registered" in response.json["error"]


def test_login_route(client, init_database):
    user_data = {
        "email": "loginroute@example.com",
        "username": "loginroute",
        "password": "Password123!",
    }
    client.post("/api/auth/register", json=user_data)

    login_data = {"email": "loginroute@example.com", "password": "Password123!"}

    response = client.post("/api/auth/login", json=login_data)

    assert response.status_code == HTTP_OK
    data = response.json
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]


def test_login_invalid_credentials_route(client, init_database):
    user_data = {
        "email": "invalidroute@example.com",
        "username": "invalidroute",
        "password": "Password123!",
    }
    client.post("/api/auth/register", json=user_data)

    login_data = {"email": "invalidroute@example.com", "password": "WrongPassword123!"}

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == HTTP_UNAUTHORIZED
    assert "error" in response.json
    assert "Invalid credentials" in response.json["error"]


def test_get_profile_route(client, init_database, auth_headers):
    response = client.get("/api/auth/profile", headers=auth_headers)

    assert response.status_code == HTTP_OK
    data = response.json
    assert "email" in data
    assert "username" in data
    assert "id" in data


def test_update_profile_route(client, init_database, auth_headers):
    update_data = {"username": "updatedusername", "email": "updated@example.com"}

    response = client.put("/api/auth/profile", json=update_data, headers=auth_headers)

    assert response.status_code == HTTP_OK
    data = response.json
    assert data["username"] == update_data["username"]
    assert data["email"] == update_data["email"]
