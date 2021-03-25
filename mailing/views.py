from mail_templated import send_mail, EmailMessage
from .models import MailModel
from user.models import User
from django.core import mail

# Create your views here.


def sendMail(template, from_email, to_email):
    try:
        user = User.objects.get(email=to_email)
    except User.DoesNotExist:
        user = None

    if user != None:
        message = EmailMessage(template, {'user': user}, from_email, [user.email])
    else:
        message = EmailMessage(template, {}, from_email, [to_email])

    message.load_template()
    message.render()
    MailModel.objects.create(
            user = user,
            to_email = to_email,
            from_email = from_email,
            subject = message.subject,
            message = message.body,
        )
    message.send()