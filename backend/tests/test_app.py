"""
Basic smoke tests for the Document Intelligence System
"""
import os
import sys
import warnings

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        import numpy
        import requests
        print("✓ Core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_module_imports():
    """Test that application modules can be imported"""
    print("\nTesting application module imports...")
    try:
        import routes
        import auth
        import query
        import upload
        import tasks

        print("✓ Core application modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Module import error: {e}")
        return False


def test_fastapi_app():
    """Test that FastAPI app initializes correctly"""
    print("\nTesting FastAPI app initialization...")
    try:
        from main import app
        print(f"✓ FastAPI app initialized: {app.title}")
        return True
    except Exception as e:
        print(f"✗ FastAPI app error: {e}")
        return False


def test_health_endpoint():
    """Test health check endpoint"""
    print("\nTesting health check endpoint...")
    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)
        response = client.get("/health")

        if response.status_code == 200 and response.json()["status"] == "ok":
            print("✓ Health check endpoint working")
            return True
        print(f"✗ Health check returned unexpected response: {response.json()}")
        return False
    except Exception as e:
        print(f"✗ Health check test error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Document Intelligence System - Test Suite")
    print("=" * 60)

    tests = [
        test_imports,
        test_module_imports,
        test_fastapi_app,
        test_health_endpoint,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)

    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
