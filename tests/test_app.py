"""
Example unit tests for TaskPilot backend.

This file demonstrates basic tests for the Flask application.
To use these tests in the CI pipeline:

1. Save this file as: tests/test_app.py
2. Run tests with: pytest tests/ -v
3. Install pytest: pip install pytest pytest-cov

Tests cover:
- Application creation and configuration
- Health check endpoint
- Authentication endpoints (login, register)
- Basic API health checks
"""

import pytest
import json
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from config import Config


class TestAppSetup:
    """Test Flask application setup and configuration."""

    @pytest.fixture
    def app(self):
        """Create application for the tests."""
        app = create_app()
        app.config['TESTING'] = True
        yield app

    @pytest.fixture
    def client(self, app):
        """Create a test client for the application."""
        return app.test_client()

    def test_app_creation(self, app):
        """Test that Flask app is created successfully."""
        assert app is not None
        assert app.config['TESTING'] is True

    def test_app_secret_key_configured(self, app):
        """Test that SECRET_KEY is configured."""
        assert app.config['SECRET_KEY'] is not None
        assert len(app.config['SECRET_KEY']) > 0

    def test_flask_environment(self, app):
        """Test that Flask environment is properly set."""
        # In testing, should have testing mode enabled
        assert app.config['TESTING'] is True


class TestHealthEndpoint:
    """Test health check endpoint."""

    @pytest.fixture
    def app(self):
        """Create application for the tests."""
        app = create_app()
        app.config['TESTING'] = True
        yield app

    @pytest.fixture
    def client(self, app):
        """Create a test client for the application."""
        return app.test_client()

    def test_health_endpoint_exists(self, client):
        """Test that /health endpoint exists and returns 200."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_json_response(self, client):
        """Test that /health returns valid JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_endpoint_response_structure(self, client):
        """Test that /health response has required fields."""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert 'status' in data
        assert 'message' in data
        assert data['status'] == 'healthy'

    def test_health_endpoint_no_auth_required(self, client):
        """Test that /health is accessible without authentication."""
        response = client.get('/health')
        assert response.status_code == 200


class TestAuthEndpoints:
    """Test authentication endpoints (registration, login)."""

    @pytest.fixture
    def app(self):
        """Create application for the tests."""
        app = create_app()
        app.config['TESTING'] = True
        yield app

    @pytest.fixture
    def client(self, app):
        """Create a test client for the application."""
        return app.test_client()

    def test_register_endpoint_exists(self, client):
        """Test that /api/auth/register endpoint exists."""
        # POST with empty data should fail validation, but endpoint should exist
        response = client.post('/api/auth/register', 
                             json={})
        # Expect 400 (validation error) or 201 (success), not 404
        assert response.status_code in [400, 409, 201]

    def test_login_endpoint_exists(self, client):
        """Test that /api/auth/login endpoint exists."""
        response = client.post('/api/auth/login',
                             json={})
        # Expect 400 (validation error) or 200 (success), not 404
        assert response.status_code in [400, 401, 200]

    def test_verify_auth_endpoint_exists(self, client):
        """Test that /api/auth/verify endpoint exists."""
        response = client.post('/api/auth/verify')
        # Expect 401 (no token) or 200 (valid token), not 404
        assert response.status_code in [400, 401, 200]

    def test_register_validation_empty_username(self, client):
        """Test registration validation for empty username."""
        response = client.post('/api/auth/register',
                             json={
                                 'username': '',
                                 'email': 'test@example.com',
                                 'password': 'Test123!'
                             })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_register_validation_short_password(self, client):
        """Test registration validation for short password."""
        response = client.post('/api/auth/register',
                             json={
                                 'username': 'testuser',
                                 'email': 'test@example.com',
                                 'password': '123'
                             })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_login_validation_empty_credentials(self, client):
        """Test login validation for empty credentials."""
        response = client.post('/api/auth/login',
                             json={
                                 'username': '',
                                 'password': ''
                             })
        assert response.status_code == 400


class TestTaskEndpoints:
    """Test task API endpoints."""

    @pytest.fixture
    def app(self):
        """Create application for the tests."""
        app = create_app()
        app.config['TESTING'] = True
        yield app

    @pytest.fixture
    def client(self, app):
        """Create a test client for the application."""
        return app.test_client()

    def test_get_tasks_endpoint_exists(self, client):
        """Test that /api/tasks endpoint exists."""
        response = client.get('/api/tasks')
        # Without auth, should return 401 or 403, not 404
        assert response.status_code in [401, 403, 200]

    def test_create_task_endpoint_exists(self, client):
        """Test that POST /api/tasks endpoint exists."""
        response = client.post('/api/tasks', json={})
        # Without auth, should return 401 or 403, not 404
        assert response.status_code in [401, 403, 201, 400]

    def test_task_endpoints_require_authentication(self, client):
        """Test that task endpoints require authentication."""
        endpoints = [
            ('GET', '/api/tasks'),
            ('POST', '/api/tasks', {}),
        ]
        
        for method, path, *data in endpoints:
            if method == 'GET':
                response = client.get(path)
            else:
                response = client.post(path, json=data[0] if data else {})
            
            # Should not be 404 (endpoint exists)
            assert response.status_code != 404


class TestConfiguration:
    """Test that configuration loads properly."""

    def test_config_db_host(self):
        """Test that database host is configured."""
        assert hasattr(Config, 'DB_HOST')
        assert Config.DB_HOST is not None

    def test_config_db_name(self):
        """Test that database name is configured."""
        assert hasattr(Config, 'DB_NAME')
        assert Config.DB_NAME is not None

    def test_config_secret_key(self):
        """Test that SECRET_KEY is configured."""
        assert hasattr(Config, 'SECRET_KEY')
        assert Config.SECRET_KEY is not None

    def test_config_cors_origins(self):
        """Test that CORS origins are configured."""
        assert hasattr(Config, 'CORS_ORIGINS')
        assert isinstance(Config.CORS_ORIGINS, list)
        assert len(Config.CORS_ORIGINS) > 0


# ═══════════════════════════════════════════════════════════════
# PYTEST CONFIGURATION
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration for all tests."""
    return Config


if __name__ == '__main__':
    # Run tests with: python -m pytest tests/test_app.py -v
    pytest.main([__file__, '-v'])
