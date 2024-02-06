import pytest

from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(vote)
    session.commit()


def test_vote_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/sqlalchemy/votes/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 201


def test_vote_post_twice(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/sqlalchemy/votes/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409


def test_unauthorized_user_vote_post(client, test_posts):
    response = client.post(
        "/sqlalchemy/votes/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 401


def test_vote_post_non_exist(authorized_client, test_posts):
    response = authorized_client.post(
        "/sqlalchemy/votes/", json={"post_id": 888888, "dir": 1}
    )
    assert response.status_code == 404


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/sqlalchemy/votes/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post(
        "/sqlalchemy/votes/", json={"post_id": 888888, "dir": 0}
    )
    assert response.status_code == 404
