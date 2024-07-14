from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from tests.helpers import create_user


@pytest.mark.integration
def test_create_user_api(client: TestClient):
    response = client.post(
        '/auth/register',
        json={
            'username': 'test_user',
            'email': 'test_user@email.com',
            'password': 'test_password'
        })

    response_json = response.json()
    assert response.status_code == 201
    assert response_json['status'] == 'success'
    assert response_json['message'] == 'User created successfully'
    assert 'id' in response_json['data']
    assert response_json['data']['username'] == 'test_user'
    assert response_json['data']['email'] == 'test_user@email.com'
    assert 'created_at' in response_json['data']
    assert 'password' not in response_json['data']


@pytest.mark.integration
def test_create_user_api_should_return_error_when_user_already_exists(
    client: TestClient,
    db_session: Session
):
    create_user(db_session)

    response = client.post(
        '/auth/register',
        json={
            'username': 'test_user',
            'email': 'testuser@email.com',
            'password': 'test_password'
        })

    response_json = response.json()
    print(response_json)
    assert response.status_code == 400
    assert response_json['detail'] == 'User already exists'
