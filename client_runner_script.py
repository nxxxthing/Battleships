"""
Test client for the api
"""
import requests

# Define the base URL
BASE_URL = "http://localhost:8000"

# Define the endpoint paths
TESTDATA_ENDPOINT = "/testdata"
SOLVE_ENDPOINT = "/solve"

try:
    # Get test data
    response = requests.get(BASE_URL + TESTDATA_ENDPOINT, timeout=5)
    response.raise_for_status()  # Raise an exception for HTTP errors
    test_data_received = response.json()

    print("Test data received:")
    print(test_data_received)

    # Submit test data
    response = requests.post(BASE_URL + SOLVE_ENDPOINT, json=test_data_received, timeout=5)
    response.raise_for_status()  # Raise an exception for HTTP errors
    solution = response.json()

    print("Solution received:")
    print(solution)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
