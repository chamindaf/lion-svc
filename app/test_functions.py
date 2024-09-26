import logging
from app.workflows.email import send_email
from app.config import OTP_TEST_EMAIL, OTP_TEST_CC_EMAIL, SEND_EMAIL_URL

# Set up logging for this module
logger = logging.getLogger(__name__)

def send_test_emails(temp_password: str, first_name: str, last_name: str):
    """
    Send test emails with the temporary password.

    This function is used only for testing purposes.

    Args:
        temp_password (str): The temporary password to send.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
    """
    try:
        test_emails = [OTP_TEST_EMAIL, OTP_TEST_CC_EMAIL]
        for email in test_emails:
            send_email(
                workflow_url=SEND_EMAIL_URL,
                email=email,
                type="Temporary Password",
                body={
                    "Email": email,
                    "TempPassword": temp_password,
                    "Firstname": first_name,
                    "Lastname": last_name
                }
            )
            logger.info(f"Test email sent to {email}.")
    except Exception as e:
        logger.error(f"Error sending test emails: {e}")