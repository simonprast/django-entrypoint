from mail_templated import send_mail
from .models import MailModel

# Create your views here.


def sendMail(template, user, from_email):
    MailModel.objects.create(user=user, template=template, from_email=from_email)
    send_mail(template, {'user': user}, from_email, [user.email], fail_silently=False)
