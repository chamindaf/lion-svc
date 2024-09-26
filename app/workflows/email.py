import requests
import logging
import time

# Set up logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Adjust the level based on your needs

def send_email(workflow_url: str, email: str, body: dict, type: str, retries: int = 3, backoff_factor: float = 0.5) -> dict:
    """
    Sends an OTP to the specified email using an external API with retry mechanism.

    Args:
        email (str): The recipient's email address.
        otp (int): The OTP code to be sent.
        retries (int): Number of retry attempts in case of failure.
        backoff_factor (float): Factor by which to increase wait time between retries.

    Returns:
        dict: The API response if successful, or an error message if the request fails.
    """

    # Prepare the payload (body) for the POST request
    payload = body

    # Prepare the headers for the POST request
    headers = {
        "Content-Type": "application/json"
    }

    attempt = 0
    while attempt < retries:
        try:
            # Log the action of sending the request
            logger.info(f"Attempt {attempt + 1}: Sending {type} to {email}")

            # Send the POST request to the API
            response = requests.post(workflow_url, json=payload, headers=headers)

            # Check the response status code
            response.raise_for_status()

            # Log and return the successful response
            logger.info(f"{type} sent successfully to {email}. Response: {response.json()}")
            return {"status": "success", "response": response.json()}

        except requests.exceptions.HTTPError as http_err:
            # Log the HTTP error, including response details
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            if response.status_code == 502:
                # If it's a 502 error, retry after a delay
                logger.warning(f"Received 502 Bad Gateway. Retrying in {backoff_factor * (attempt + 1)} seconds...")
                time.sleep(backoff_factor * (attempt + 1))
            else:
                # If it's another HTTP error, return immediately
                return {"status": "failure", "error": str(http_err), "response": response.text}

        except requests.exceptions.RequestException as req_err:
            # Log and return a general request exception
            logger.error(f"Request failed: {req_err}")
            return {"status": "failure", "error": str(req_err)}

        except Exception as err:
            # Log and return any other general exceptions
            logger.error(f"An unexpected error occurred: {err}")
            return {"status": "failure", "error": str(err)}

        attempt += 1

    # If all retry attempts fail, return failure
    logger.error(f"Failed to send {type} to {email} after {retries} attempts.")
    return {"status": "failure", "error": "Max retries exceeded."}
