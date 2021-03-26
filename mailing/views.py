from mail_templated import EmailMessage
from .models import MailModel
from user.models import User
from django.core import mail

from francy.settings import DEFAULT_FROM_EMAIL

# Create your views here.

# sendMail sends an email and saves it into the database.
def sendMail(template, from_email, to_email):
    try:
        user = User.objects.get(email=to_email)
    except User.DoesNotExist:
        user = None

    if user != None:
        message = EmailMessage(template, {'user': user}, from_email, [user.email])
    else:
        message = EmailMessage(template, {}, from_email, [to_email])

    if from_email == None or from_email == '':
        from_email = DEFAULT_FROM_EMAIL

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
    