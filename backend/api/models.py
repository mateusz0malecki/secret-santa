import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class SantaGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    budget_limit = models.IntegerField()
    santa_day = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.created_at}"


class SantaUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)
    group = models.ForeignKey(
        SantaGroup,
        on_delete=models.CASCADE,
        related_name="santa_users",
        blank=True,
        null=True,
        default=None
    )
    secret_santa = models.EmailField(max_length=254, blank=True, null=True, default=None)
    list_written = models.BooleanField(default=False, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.email} - {self.created_at} - group: {self.group.name} - {self.group.id}"


class SantaList(models.Model):
    santa_user = models.OneToOneField(
        SantaUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.santa_user} - {self.created_at}"
