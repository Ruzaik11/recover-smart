from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
import logging

logger = logging.getLogger("myapp")

def create_user_and_send_email(user):
    try:
        password = get_random_string(10)  # Generate a random password
        user.set_password(password)  # Securely set the password
        user.save()

        logger.info(f"Password: {password}")

        return True

        context = {
            "first_name": user.first_name,
            "username": user.username,
            "password": password,
        }
        

        html_content = render_to_string("emails/welcome_email.html", context)  # Render the HTML email template
        subject = "Your New Account Details"
        text_content = f"Hello {user.first_name},\n\nYour account has been created successfully!\n\nUsername: {user.username}\nPassword: {password}\n\nPlease change your password after logging in."

        # Create the email message with both plain text and HTML content
        email = EmailMultiAlternatives(
            subject,
            text_content,
            'from@example.com',  # Replace with your actual sender email
            [user.email]
        )
        email.attach_alternative(html_content, "text/html")  # Attach the HTML version
        email.send()  # Send the email

        return user
    except Exception as e:
        raise ValueError(f"Error creating user: {str(e)}")
