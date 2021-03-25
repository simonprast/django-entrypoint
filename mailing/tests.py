from django.test import TestCase
from .views import sendMail
from user.models import User
from .models import MailModel

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
        user = User.objects.get_by_natural_key('test1')
        sendMail('mailing/plain.tpl', user, None)
