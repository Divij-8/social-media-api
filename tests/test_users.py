import pytest
from app import models
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to my Social Media API! Deployed via Render."}


def test_create_user(client):
    res = client.post(
        "/signup", 
        json={"email": "hello@gmail.com", "password": "password123", "username": "hello"}
    )
    new_user = res.json()
    assert res.status_code == 201
    assert new_user["email"] == "hello@gmail.com"
    assert new_user["username"] == "hello"
    assert "password" not in new_user  


def test_login_user(client, test_user):
    res = client.post(
        "/login", 
        data={"username": test_user["username"], "password": test_user["password"]}
    )
    login_res = res.json()
    assert res.status_code == 200
    assert login_res["token_type"] == "bearer"
    assert "access_token" in login_res


def test_login_incorrect_password(client, test_user):
    res = client.post(
        "/login", 
        data={"username": test_user["username"], "password": "WRONG_PASSWORD"}
    )
    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid Credentials"


def test_create_user_duplicate_email(client, test_user):
    res = client.post(
        "/signup", 
        json={"email": test_user["email"], "password": "password123", "username": "othername"}
    )
    assert res.status_code == 409  