from app.config import settings
import pytest
from app.schemas.post import PostResponse, PostResponseWithPagination

def test_create_post_success(client, authorized_client):
    """Test creating a new post via
    API."""
    client, headers = authorized_client()
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content."
    }
    response = client.post(f"{settings.API_PREFIX}/posts/", json=post_data, headers=headers)
    assert response.status_code == 201
    created_post = PostResponse(**response.json())
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]
    assert created_post.id is not None
    assert created_post.created_at is not None

def test_get_post_success(client, authorized_client):
    """Test retrieving a post via API."""
    client, headers = authorized_client()
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content."
    }
    create_response = client.post(f"{settings.API_PREFIX}/posts/", json=post_data, headers=headers)
    assert create_response.status_code == 201
    created_post = PostResponse(**create_response.json())

    get_response = client.get(f"{settings.API_PREFIX}/posts/{created_post.id}", headers=headers)
    assert get_response.status_code == 200
    retrieved_post = PostResponse(**get_response.json())
    assert retrieved_post.title == post_data["title"]
    assert retrieved_post.content == post_data["content"]
    assert retrieved_post.id == created_post.id

def test_get_all_posts_success(client, authorized_client):
    """Test retrieving all posts via API."""
    client, headers = authorized_client()
    post_data1 = {
        "title": "Test Post 1",
        "content": "This is the first test post content."
    }
    post_data2 = {
        "title": "Test Post 2",
        "content": "This is the second test post content."
    }
    client.post(f"{settings.API_PREFIX}/posts/", json=post_data1, headers=headers)
    client.post(f"{settings.API_PREFIX}/posts/", json=post_data2, headers=headers)

    response = client.get(f"{settings.API_PREFIX}/posts/", headers=headers)
    assert response.status_code == 200
    posts = PostResponseWithPagination(**response.json())
    assert len(posts.posts) >= 2
    titles = [post.title for post in posts.posts]
    assert post_data1["title"] in titles
    assert post_data2["title"] in titles
    contents = [post.content for post in posts.posts]
    assert post_data1["content"] in contents
    assert post_data2["content"] in contents
