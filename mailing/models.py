from django.db import models

from user.models import User

# Create your models here.

class MailModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    to_email = models.EmailField(blank=False, null=True)
    from_email = models.EmailField(blank=True, null=True)
    subject = models.TextField(null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.user.username
