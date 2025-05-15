import os
import requests
import pytest
import logging
import allure
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "https://api.staging.krishivaas.ai")

# Test credentials from environment variables
TEST_USER = {
    "email": os.getenv("TEST_EMAIL"),
    "password": os.getenv("TEST_PASSWORD")
}

def sanitize_response(response_text):
    """Return API responses without redacting sensitive data."""
    try:
        import json
        response_data = json.loads(response_text)
        return json.dumps(response_data, indent=2)
    except:
        return response_text

@pytest.fixture(scope="session")
def auth_token():
    """Login and return auth token with detailed Allure reporting"""
    with allure.step("Authenticating user"):
        login_url = f"{BASE_URL}/api/v1/login"
        
        # Add request details to Allure
        allure.attach(
            body=str({"email": TEST_USER["email"], "password": TEST_USER["password"]}),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON
        )
        
        try:
            response = requests.post(
                login_url,
                json=TEST_USER,
                headers={"Content-Type": "application/json"}
            )
            
            # Store response details
            response_details = {
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add full but sanitized response to Allure
            allure.attach(
                body=response.text,
                name="Full Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Assertions
            assert response.status_code == 200, f"Login failed with {response.status_code}"
            token = response.json().get("token")
            assert token, "No token received in login response"
            
            logger.info("Successfully obtained authentication token")
            return token
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            pytest.fail(f"Authentication failed: {str(e)}")

@allure.feature("Authentication")
@allure.story("Login API")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Test User Login")
def test_login_api(auth_token):
    """Test login API with detailed Allure reporting"""
    assert auth_token, "Authentication token validation failed"
    logger.info("Login API test completed successfully")

@allure.feature("Organization")
@allure.story("Organization Details")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Get Single Organization Detail")
def test_get_single_organization_detail():
    """Test GET single organization detail API"""
    url = f"{BASE_URL}/api/v1/get-single-organization-detail"
    auth_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmtyaXNoaXZhYXMuYWkvYXBpL3YxL2xvZ2luIiwiaWF0IjoxNzQ3MjE2MzQyLCJleHAiOjE3NDk4MDgzNDIsIm5iZiI6MTc0NzIxNjM0MiwianRpIjoiVkJKdGJ4YmdFUVN4bmo2NCIsInN1YiI6IjEzODQiLCJwcnYiOiJmZjY2ZDA3ZjZkNDYyNzMzYmIyOWMzN2QyYTU5YmViZjZiZDY2NjQwIn0.OXzxNUpXpnoxl20s9B_-imreypJ07SZYXkkUD2EuSO0"
    params = {
        "org_id": 48,
        "token": auth_token
    }
    
    with allure.step("Request organization details"):
        try:
            response = requests.get(url, params=params)
            
            # Add full request details (sanitized)
            allure.attach(
                body=str({"org_id": params["org_id"], "token": "***REDACTED***"}),
                name="Request Parameters",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Add full response to Allure
            allure.attach(
                body=sanitize_response(response.text),
                name="Complete Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Also add formatted response for better readability
            allure.attach(
                body=f"Status Code: {response.status_code}\n\nResponse:\n{sanitize_response(response.text)}",
                name="Formatted Response",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"Organization detail response: {response.status_code}")
            
            # Assertions
            assert response.status_code == 200, \
                f"Expected status 200, got {response.status_code}"
            assert response.json().get("success"), \
                "API did not return success=True"
                
        except Exception as e:
            logger.error(f"Organization detail request failed: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}")

@allure.feature("Organization")
@allure.story("Organization Data")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Get Organization Information")
def test_get_organization():
    """Test organization data retrieval"""
    url = f"{BASE_URL}/api/v1/get-organizition"
    params = {"org_id": 48, "ogs_id": 115}
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmtyaXNoaXZhYXMuYWkvYXBpL3YxL2xvZ2luIiwiaWF0IjoxNzQ3MjE2MzQyLCJleHAiOjE3NDk4MDgzNDIsIm5iZiI6MTc0NzIxNjM0MiwianRpIjoiVkJKdGJ4YmdFUVN4bmo2NCIsInN1YiI6IjEzODQiLCJwcnYiOiJmZjY2ZDA3ZjZkNDYyNzMzYmIyOWMzN2QyYTU5YmViZjZiZDY2NjQwIn0.OXzxNUpXpnoxl20s9B_-imreypJ07SZYXkkUD2EuSO0"
    headers = {"Authorization": f"Bearer {auth_token}"}

    with allure.step("Making organization data request"):
        try:
            # Debug logging
            logger.info(f"Requesting organization data from {url}")
            
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            # Attach complete request details (sanitized)
            allure.attach(
                body=f"URL: {url}\nHeaders: { {k: '***REDACTED***' if 'auth' in k.lower() else v for k, v in headers.items()} }\nParams: {params}",
                name="Complete Request Details",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Attach full response
            allure.attach(
                body=sanitize_response(response.text),
                name="Complete API Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Attach formatted response
            allure.attach(
                body=f"Status: {response.status_code}\nHeaders: {dict(response.headers)}\n\nBody:\n{sanitize_response(response.text)}",
                name="Formatted Response with Headers",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            # Assertions
            assert response.status_code == 200, \
                f"Expected 200, got {response.status_code}"
            assert "success" in response.json(), \
                "Response missing 'success' field"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            pytest.fail(f"Request failed: {str(e)}")