import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def authenticate_user(api_client, create_user):
    def make_authenticated_user(**kwargs):
        user = create_user(**kwargs)
        api_client.force_authenticate(user=user)
        return user
    return make_authenticated_user

@pytest.fixture
def create_todo():
    def make_todo(**kwargs):
        return Todo.objects.create(**kwargs)
    return make_todo

@pytest.mark.django_db
def test_create_todo(api_client, authenticate_user):
    user = authenticate_user(username="testuser", password="testpassword")
    url = reverse("todo:api-v1:todo-list")
    data = {
        "title": "New Todo",
        "description": "New Description",
        "due_date": "2023-12-31",
        "done": False,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Todo.objects.filter(title="New Todo").exists()

@pytest.mark.django_db
def test_update_todo(api_client, authenticate_user, create_todo):
    user = authenticate_user(username="testuser", password="testpassword")
    todo = create_todo(user=user, title="Old Todo", description="Old Description", due_date="2023-12-31", done=False)
    url = reverse("todo:api-v1:todo-detail", args=[todo.id])
    data = {
        "title": "Updated Todo",
        "description": "Updated Description",
        "due_date": "2023-12-31",
        "done": True,
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    todo.refresh_from_db()
    assert todo.title == "Updated Todo"
    assert todo.description == "Updated Description"
    assert todo.done

@pytest.mark.django_db
def test_delete_todo(api_client, authenticate_user, create_todo):
    user = authenticate_user(username="testuser", password="testpassword")
    todo = create_todo(user=user, title="Test Todo", description="Test Description", due_date="2023-12-31", done=False)
    url = reverse("todo:api-v1:todo-detail", args=[todo.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Todo.objects.filter(id=todo.id).exists()

@pytest.mark.django_db
def test_retrieve_todo_list(api_client, authenticate_user, create_todo):
    user = authenticate_user(username="testuser", password="testpassword")
    create_todo(user=user, title="Test Todo 1", description="Test Description 1", due_date="2023-12-31", done=False)
    create_todo(user=user, title="Test Todo 2", description="Test Description 2", due_date="2023-12-31", done=True)
    url = reverse("todo:api-v1:todo-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["title"] == "Test Todo 1"
    assert response.data["results"][1]["title"] == "Test Todo 2"
