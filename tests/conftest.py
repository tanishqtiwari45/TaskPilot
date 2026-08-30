"""
Pytest configuration and shared fixtures for TaskPilot tests.

This file is automatically discovered by pytest and provides:
- Shared fixtures for all tests
- Test setup and teardown
- Test configuration
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture(scope="session")
def test_session():
    """
    Session-wide fixture for test environment setup.
    Runs once per test session.
    """
    print("\n" + "="*60)
    print("Starting TaskPilot Test Suite")
    print("="*60)
    
    # Setup: any module-level imports or initializations
    yield
    
    # Teardown: cleanup after all tests
    print("\n" + "="*60)
    print("Completed TaskPilot Test Suite")
    print("="*60)


@pytest.fixture(scope="function")
def cleanup():
    """
    Function-level fixture for per-test cleanup.
    Runs before and after each test.
    """
    # Setup: runs before each test
    yield
    # Teardown: runs after each test
    pass


@pytest.fixture(autouse=True)
def reset_modules():
    """
    Automatically reset imported modules between tests.
    Helps avoid test pollution.
    """
    yield
    # After each test, you can add cleanup code here if needed


# ═══════════════════════════════════════════════════════════════
# PYTEST HOOKS
# ═══════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Configure pytest."""
    print("\nConfiguring pytest...")
    print(f"Python: {sys.version}")
    print(f"Pytest: {pytest.__version__}")


def pytest_sessionstart(session):
    """Start of test session."""
    print(f"\nTest session started: {session.name}")


def pytest_sessionfinish(session, exitstatus):
    """End of test session."""
    if exitstatus == 0:
        print("\n[PASS] All tests passed!")
    else:
        print(f"\n[FAIL] Tests failed with exit status: {exitstatus}")


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Automatically mark slow tests if they contain "slow" in name
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)


# ═══════════════════════════════════════════════════════════════
# CUSTOM ASSERTIONS & HELPERS
# ═══════════════════════════════════════════════════════════════

class AssertionHelpers:
    """Helper functions for test assertions."""
    
    @staticmethod
    def assert_valid_json_response(response):
        """Assert that response is valid JSON."""
        assert response.content_type == 'application/json', \
            f"Expected JSON response, got {response.content_type}"
        try:
            response.get_json()
        except Exception as e:
            pytest.fail(f"Response is not valid JSON: {e}")
    
    @staticmethod
    def assert_has_required_fields(data, required_fields):
        """Assert that dictionary has all required fields."""
        for field in required_fields:
            assert field in data, f"Required field '{field}' not found in response"


@pytest.fixture
def assert_helpers():
    """Provide assertion helpers to tests."""
    return AssertionHelpers()
