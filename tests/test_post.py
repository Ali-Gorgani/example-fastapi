import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/sqlalchemy/posts")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, response.json())
    posts_list = list(posts_map)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/sqlalchemy/posts")
    assert response.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/sqlalchemy/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/sqlalchemy/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/sqlalchemy/posts/888888")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "title, content, published", [
        ("awesome title", "awesome content", True),
        ("fantastic title", "fantastic content", False),
        ("great title", "great content", True),
    ]
)
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post(
        "/sqlalchemy/posts",
        json={"title": title, "content": content, "published": published},
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        "/sqlalchemy/posts",
        json={"title": "arbitrary title", "content": "arbitrary content"},
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post(
        "/sqlalchemy/posts",
        json={"title": "arbitrary title", "content": "arbitrary content"},
    )
    assert response.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/sqlalchemy/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/sqlalchemy/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/sqlalchemy/posts/888888")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/sqlalchemy/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/sqlalchemy/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = client.put(f"/sqlalchemy/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 401


def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = authorized_client.put(f"/sqlalchemy/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_other_user_post(client, test_user, test_user_2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = client.put(f"/sqlalchemy/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/sqlalchemy/posts/888888", json=data)
    assert response.status_code == 404
