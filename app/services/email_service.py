import os
from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi
from sib_api_v3_sdk.rest import ApiException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.configuration = Configuration()
        self.configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
        self.api_client = ApiClient(self.configuration)
        self.email_api = TransactionalEmailsApi(self.api_client)
        self.sender_email = os.getenv('BREVO_SENDER_EMAIL')
        self.sender_name = os.getenv('BREVO_SENDER_NAME')

    def send_email_verification(self, to_email: str, verification_token: str, user_name: str = None) -> Dict[str, Any]:
        """Send email verification email"""
        try:
            subject = "Verify Your Email Address"
            
            # Create HTML content for email verification
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #333; text-align: center;">Email Verification</h2>
                        <p style="color: #666; line-height: 1.6;">
                            Hi {user_name or 'User'},<br><br>
                            Please click the button below to verify your email address and activate your account.
                        </p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://essay-ai-vraj-dev.netlify.app/verify-email?token={verification_token}" 
                               style="background-color: #007bff; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 5px; display: inline-block;">
                                Verify Email
                            </a>
                        </div>
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            This link will expire in 24 hours.<br>
                            If you didn't request this verification, please ignore this email.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return self._send_email(to_email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Error sending email verification: {str(e)}")
            raise e

    def send_password_reset(self, to_email: str, reset_token: str, user_name: str = None) -> Dict[str, Any]:
        """Send password reset email"""
        try:
            subject = "Reset Your Password"
            
            # Create HTML content for password reset
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #333; text-align: center;">Password Reset</h2>
                        <p style="color: #666; line-height: 1.6;">
                            Hi {user_name or 'User'},<br><br>
                            We received a request to reset your password. Click the button below to create a new password.
                        </p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="http://localhost:8000/backend/auth/reset-password?token={reset_token}" 
                               style="background-color: #dc3545; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 5px; display: inline-block;">
                                Reset Password
                            </a>
                        </div>
                        <p style="color: #999; font-size: 12px; text-align: center;">
                            This link will expire in 1 hour.<br>
                            If you didn't request this password reset, please ignore this email.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return self._send_email(to_email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Error sending password reset: {str(e)}")
            raise e

    def _send_email(self, to_email: str, subject: str, html_content: str) -> Dict[str, Any]:
        """Send email using Brevo SMTP API"""
        try:
            send_smtp_email = {
                "sender": {
                    "email": self.sender_email,
                    "name": self.sender_name
                },
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_content
            }
            
            api_response = self.email_api.send_transac_email(send_smtp_email)
            
            return {
                "success": True,
                "message_id": api_response.message_id,
                "message": "Email sent successfully"
            }
            
        except ApiException as e:
            logger.error(f"Brevo API Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send email"
            }
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send email"
            }
