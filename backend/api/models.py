import uuid
from django.db import models


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
        return f"{self.santa_user.id} - {self.created_at}"
