from django.test import TestCase, override_settings
from .views import sendMail
from user.models import User
from .models import MailModel
from django.core import mail

# Create your tests here.

class MailModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='test1',
            email='daniel.petutschnigg@gmail.com',
            password='test123',
            utype=1
        )

    def test_sendMail(self):
        sendMail('mailing/plain.tpl', None, "daniel.petutschnigg@gmail.com")
        model1 = MailModel.objects.get(to_email="daniel.petutschnigg@gmail.com")
        print(model1.subject)
        print(model1.message)
        sendMail('mailing/plain.tpl', None, "petutschnigg@gmail.com")
        model2 = MailModel.objects.get(to_email="petutschnigg@gmail.com")
        print(model2.subject)
        print(model2.message)