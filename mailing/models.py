from django.db import models

from user.models import User

# Create your models here.


class MailModel(models.Model):
    template = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    from_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username
