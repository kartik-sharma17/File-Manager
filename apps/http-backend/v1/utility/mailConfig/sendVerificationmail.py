import resend
from jinja2 import Template
from config import settings

resend.api_key = settings.RESEND_API_KEY

async def SendVerificationEmail(email: str, name: str, token: str):
    try:
        verify_link = f"{settings.BASE_URL}/verify-account/{token}"

        with open("v1/utility/mailConfig/template/verifyMailTemplate.html") as f:
            html_template = Template(f.read())
            html_content = html_template.render(name=name, verify_link=verify_link)

        resend.Emails.send({
            "from": f"{settings.MAIL_FROM_NAME} <support@clarixai.in>",
            "to": [email],
            "subject": "Verify Your Clarix Account",
            "html": html_content,
        })

        return True
    except Exception as e:
        print(f"somethings went wrong whiling sending email {e}")
        return False


