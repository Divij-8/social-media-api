import pytest
from app import models 

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    assert res.status_code == 200
    assert len(res.json()) == 4

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = res.json()
    
    assert res.status_code == 200
    assert post["post"]["id"] == test_posts[0].id
    assert post["post"]["content"] == test_posts[0].content

def test_create_post(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"}
    )
    created_post = res.json()
    
    assert res.status_code == 201
    assert created_post["title"] == "arbitrary title"
    assert created_post["user_id"] == test_user['id']

def test_unauthorized_user_create_post(client, test_user):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"}
    )
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/88888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = res.json()
    assert res.status_code == 200
    assert updated_post["title"] == data["title"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403