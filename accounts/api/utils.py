import threading
from mail_templated import EmailMessage
from django.conf import settings


class EmailThread(threading.Thread):  # Fix spelling from EmailThead to EmailThread
    def __init__(self, subject, template_name, context):
        self.subject = subject
        self.template_name = template_name
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        try:
            email = EmailMessage(
                template_name=self.template_name,
                context=self.context,
                subject=self.subject,  # Add subject
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.context["email"]],
            )
            email.send()
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
