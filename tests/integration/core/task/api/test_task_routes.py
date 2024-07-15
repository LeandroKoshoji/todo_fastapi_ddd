from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from tests.helpers import create_tasks


@pytest.mark.integration
def test_create_task(client: TestClient, auth_headers):
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "status": "pending",
            "description": "Test description",
            "send_notification": True
        },
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 201
    assert response_json["status"] == "success"
    assert response_json["message"] == "Task created successfully"
    assert response_json["data"]["title"] == "Test task"
    assert response_json["data"]["status"] == "pending"
    assert response_json["data"]["description"] == "Test description"
    assert response_json["data"]["send_notification"] is True


@pytest.mark.integration
def test_edit_task(
    client: TestClient,
    test_user,
    auth_headers,
    db_session: Session
):
    task = create_tasks(db_session, 1, user_id=test_user.id)[0]
    response = client.put(
        f"/tasks/{task.id}",
        json={
            "title": "Test task edited",
            "status": "done",
            "description": "Test description edited",
            "send_notification": False
        },
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Task edited successfully"
    assert response_json["data"]["title"] == "Test task edited"
    assert response_json["data"]["status"] == "done"
    assert response_json["data"]["description"] == "Test description edited"
    assert response_json["data"]["send_notification"] is False


@pytest.mark.integration
def test_delete_task(
    client: TestClient,
    test_user,
    auth_headers,
    db_session: Session
):
    task = create_tasks(db_session, 1, user_id=test_user.id)[0]
    response = client.delete(
        f"/tasks/{task.id}",
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Task deleted successfully"
    assert response_json["data"] == None


@pytest.mark.integration
def test_list_all_tasks(
    client: TestClient,
    test_user,
    auth_headers,
    db_session: Session
):
    tasks = create_tasks(db_session, 3, user_id=test_user.id)
    response = client.get(
        "/tasks/",
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Tasks retrieved successfully"
    assert len(response_json["data"]) == 3
    assert response_json["data"][0]["title"] == tasks[0].title
    assert response_json["data"][1]["title"] == tasks[1].title
    assert response_json["data"][2]["title"] == tasks[2].title


@pytest.mark.integration
def test_list_task_by_id(
    client: TestClient,
    test_user,
    auth_headers,
    db_session: Session
):
    tasks = create_tasks(db_session, 3, user_id=test_user.id)
    response = client.get(
        f"/tasks/{tasks[0].id}",
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Task retrieved successfully"
    assert response_json["data"]["title"] == tasks[0].title
    assert response_json["data"]["description"] == tasks[0].description
    assert response_json["data"]["status"] == tasks[0].status
    assert response_json["data"]["send_notification"] == tasks[0].send_notification


@pytest.mark.integration
def test_search_tasks(
    client: TestClient,
    test_user,
    auth_headers,
    db_session: Session
):
    create_tasks(db_session, 3, user_id=test_user.id, status="pending")
    create_tasks(db_session, 3, user_id=test_user.id, status="on_going")
    create_tasks(db_session, 3, user_id=test_user.id, status="done")

    response = client.get(
        "/tasks/search/",
        params={
            "status": "pending",
            'page': 1,
            'per_page': 10
        },
        headers=auth_headers
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Tasks retrieved successfully"
    assert len(response_json["data"]) == 3
    assert response_json["total"] == 3
    assert response_json["page"] == 1
    assert response_json["per_page"] == 10
    tasks_in_respose = [task["status"] for task in response_json["data"]]
    assert all(status == "pending" for status in tasks_in_respose)
