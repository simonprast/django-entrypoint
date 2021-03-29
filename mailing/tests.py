from django.test import TestCase
from .views import sendMail


class MailModelTest(TestCase):
    def test_sendMail(self):
        sendMail('mailing/plain.tpl', None, "daniel.petutschnigg@gmail.com")
        sendMail('mailing/plain.tpl', None, "petutschnigg@gmail.com")
