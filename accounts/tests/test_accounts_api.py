import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_registration(api_client):
    url = reverse('accounts:api-v1:register')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword123@!',
        'password1': 'newpassword123@!'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_login(api_client, create_user):
    user = create_user(username='testuser', password='testpassword123@!', email='testuser@example.com', is_verified= True)
    url = reverse('accounts:api-v1:token-login')
    data = {
        'username': 'testuser',
        'password': 'testpassword123@!'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'token' in response.data

@pytest.mark.django_db
def test_logout_with_token(api_client, create_user):
    user = create_user(username='testuser', password='testpassword123@!', email='testuser@example.com')
    
    from rest_framework.authtoken.models import Token
    token, created = Token.objects.get_or_create(user=user)

    print("Manually created token:", token.key)

    logout_url = reverse('accounts:api-v1:token-logout')
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = api_client.post(logout_url)

    assert response.status_code == 200

@pytest.mark.django_db 
def test_logout_without_token(api_client):
    logout_url = reverse('accounts:api-v1:token-logout')
    response = api_client.post(logout_url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_login_invalid_credentials(api_client, create_user):
    user = create_user(username='testuser', password='testpassword123@!', email='testuser@example.com')
    url = reverse('accounts:api-v1:token-login')
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_registration_duplicate_username(api_client, create_user):
    # Create initial user
    create_user(username='existinguser', password='testpass123', email='existing@example.com')
    
    url = reverse('accounts:api-v1:register')
    data = {
        'username': 'existinguser',
        'email': 'new@example.com',
        'password': 'newpassword123@!',
        'password1': 'newpassword123@!'
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
@pytest.mark.django_db
def test_change_password(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    url = reverse('accounts:api-v1:change-password')
    api_client.force_authenticate(user=user)
    data = {
        'old_password': 'testpassword',
        'new_password': 'newtestpassword',
        'new_password1': 'newtestpassword'
    }
    response = api_client.put(url, data)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password('newtestpassword')

@pytest.mark.django_db
def test_email_verification(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    url = reverse('accounts:api-v1:resend-verification-email')
    data = {
        'email': 'testuser@example.com'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
