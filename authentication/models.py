import secrets
import django.utils.timezone as timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Token(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=12, unique=True, editable=False)
    used = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(9)[:12]
        if not self.expiration_date:
            self.expiration_date = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiration_date

    def __str__(self):
        return self.token


@receiver(post_save, sender=CustomUser)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
