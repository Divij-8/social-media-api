import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from app.main import app
from app.database import get_session
from app.oauth2 import create_access_token
from app import models


sqlite_file_name = "database.db"
sqlite_url = "sqlite:///test.db"  

engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=None
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session 
        
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "password123", "username": "testuser"}
    res = client.post("/signup", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"] 
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# append to tests/conftest.py

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com", "password": "password123", "username": "testuser2"}
    res = client.post("/signup", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user2['id'] # Belong to different user
    }]

    

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    
    posts = session.exec(select(models.Post)).all()
    return posts