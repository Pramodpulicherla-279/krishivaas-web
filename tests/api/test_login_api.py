import requests
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.staging.krishivaas.ai"

# Test credentials
TEST_USER = {
    "email": "dmart@yopmail.com",
    "password": "Dmart@!2024"
}

@pytest.fixture(scope="function")
def auth_token(request):
    """Login and return auth token and response details"""
    login_url = f"{BASE_URL}/api/v1/login"
    response = requests.post(login_url, json=TEST_USER)
    
    # Log response details
    logger.info(f"Login Response: {response.status_code} - {response.text}")
    
    # Store response details in the request node
    request.node.response_details = {
        'status_code': response.status_code,
        'response_text': response.text
    }
    
    # Add response details to pytest-html extras (corrected version)
    if hasattr(request.node.config, "_html"):
        request.node.config._html.extras.append({
            "name": "Login Response",
            "content": f"Status: {response.status_code}\n{response.text}"
        })
    
    # Assertions
    assert response.status_code == 200, f"Login failed with {response.status_code}"
    token = response.json().get("token")
    assert token, "No token received in login response"
    return token

def test_login_api(auth_token, request):
    """Test login API and print response in pytest report"""
    # Access the response details from the request node
    response_details = request.node.response_details
    
    # Print response details to console
    print("\n--- Login API Response ---")
    print(f"Status Code: {response_details['status_code']}")
    print(f"Response Text: {response_details['response_text']}")
    
    # Log response details for pytest report
    logger.info("--- Login API Response ---")
    logger.info(f"Status Code: {response_details['status_code']}")
    logger.info(f"Response Text: {response_details['response_text']}")
    
    # Additional assertions can be added here if needed


def test_get_single_organization_detail():
    """Test GET single organization detail API and print response"""
    # API endpoint
    url = f"{BASE_URL}/api/v1/get-single-organization-detail"
    
    # Query parameters
    params = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmtyaXNoaXZhYXMuYWkvYXBpL3YxL2xvZ2luIiwiaWF0IjoxNzQ3MTI5NTYxLCJleHAiOjE3NDk3MjE1NjEsIm5iZiI6MTc0NzEyOTU2MSwianRpIjoidU5nRE1nMk1NWW1QWWhObSIsInN1YiI6IjEzODQiLCJwcnYiOiJmZjY2ZDA3ZjZkNDYyNzMzYmIyOWMzN2QyYTU5YmViZjZiZDY2NjQwIn0.YiidkfOzmDAyO955eWdjqRB3XCv7N9-wZCQt7Pu4VgM",
        "org_id": 48
    }
    
    # Send GET request
    response = requests.get(url, params=params)
    
    # Log response details
    logger.info(f"GET Response: {response.status_code} - {response.text}")
    
    # Print response details to console
    print("\n--- GET Single Organization Detail API Response ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_json = response.json()
    assert response_json.get("success"), "API did not return success=True"

def test_get_organization():
    """Test GET organization API and print response"""
    # API endpoint
    url = f"{BASE_URL}/api/v1/get-organizition"
    
    # Query parameters
    params = {
        "org_id": 48,
        "ogs_id": 115
    }

    # Use the provided token
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5zdGFnaW5nLmtyaXNoaXZhYXMuYWkvYXBpL3YxL2xvZ2luIiwiaWF0IjoxNzQ3MTQwNTY1LCJleHAiOjE3NDk3MzI1NjUsIm5iZiI6MTc0NzE0MDU2NSwianRpIjoiVjRMTUlkNUlLQkdwTVpCMCIsInN1YiI6IjEzODQiLCJwcnYiOiJmZjY2ZDA3ZjZkNDYyNzMzYmIyOWMzN2QyYTU5YmViZjZiZDY2NjQwIn0.C8LMFJ2L3swkV1oNM6N8rO5S2DxSzvhQWMIMhFgtAZ8"

    # Headers with the provided authentication token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Print the token to the console
    print(f"\n--- Authentication Token ---")
    print(f"Auth Token: {token}")
    
    # Send GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Log response details
    logger.info(f"GET Response: {response.status_code} - {response.text}")
    
    # Print response details to console
    print("\n--- GET Organization API Response ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_json = response.json()
    assert response_json.get("success"), "API did not return success=True"
