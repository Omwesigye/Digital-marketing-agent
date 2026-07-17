import os
import resend
from utils.logger import get_logger

logger = get_logger("email_tools")

class EmailManager:
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY")
        if self.api_key:
            resend.api_key = self.api_key

    def send_email(self, to: str, subject: str, html_body: str) -> dict:
        """
        Sends an email using Resend API. Falls back to mock logging if API key is missing.
        """
        logger.info(f"[EmailManager] Sending email to {to} | Subject: \"{subject}\"")
        if not self.api_key:
            logger.warning("[EmailManager] RESEND_API_KEY not set. Mocking email delivery.")
            return {"status": "success", "id": "mock-email-id-99999"}

        try:
            params = {
                "from": os.getenv("EMAIL_FROM", "onboarding@resend.dev"),
                "to": to,
                "subject": subject,
                "html": html_body
            }
            email = resend.Emails.send(params)
            return {"status": "success", "id": email.get("id")}
        except Exception as e:
            logger.error(f"[EmailManager] Resend API error: {e}")
            return {"status": "error", "error_message": str(e)}
