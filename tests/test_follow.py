import pytest
from sqlmodel import select
from app import models

def test_follow_user(authorized_client, test_user, test_user2, session):
    res = authorized_client.post(
        "/follow",
        json={"followed_id": test_user2["id"]}
    )
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully followed the user"
    
    follow = session.exec(
        select(models.Follow).where(
            models.Follow.follower_id == test_user["id"],
            models.Follow.followed_id == test_user2["id"]
        )
    ).first()
    assert follow is not None

def test_follow_self(authorized_client, test_user):
    res = authorized_client.post(
        "/follow",
        json={"followed_id": test_user["id"]}
    )
    assert res.status_code == 400
    assert "cannot follow themselves" in res.json()["detail"]

def test_follow_nonexistent_user(authorized_client, test_user):
    res = authorized_client.post(
        "/follow",
        json={"followed_id": 99999}
    )
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]

def test_follow_already_following(authorized_client, test_user, test_user2):
    res1 = authorized_client.post(
        "/follow",
        json={"followed_id": test_user2["id"]}
    )
    assert res1.status_code == 201
    
    res2 = authorized_client.post(
        "/follow",
        json={"followed_id": test_user2["id"]}
    )
    assert res2.status_code == 409
    assert "Already following" in res2.json()["detail"]

def test_unfollow_user(authorized_client, test_user, test_user2, session):
    follow_res = authorized_client.post(
        "/follow",
        json={"followed_id": test_user2["id"]}
    )
    assert follow_res.status_code == 201
    
    unfollow_res = authorized_client.delete(
        f"/unfollow/{test_user2['id']}"
    )
    assert unfollow_res.status_code == 200
    assert unfollow_res.json()["message"] == "Successfully unfollowed the user"
    
    follow = session.exec(
        select(models.Follow).where(
            models.Follow.follower_id == test_user["id"],
            models.Follow.followed_id == test_user2["id"]
        )
    ).first()
    assert follow is None

def test_unfollow_not_following(authorized_client, test_user, test_user2):
    res = authorized_client.delete(
        f"/unfollow/{test_user2['id']}"
    )
    assert res.status_code == 404
    assert "Not following" in res.json()["detail"]

def test_unfollow_self(authorized_client, test_user):
    res = authorized_client.delete(
        f"/unfollow/{test_user['id']}"
    )
    assert res.status_code == 400
    assert "Cannot unfollow yourself" in res.json()["detail"]
