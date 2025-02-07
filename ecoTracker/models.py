import uuid

from django.contrib.auth.models import User
from django.db import models


class Action(models.Model):
    class CategoryChoices(models.TextChoices):
        RECICLAGEM = "R", "Reciclagem"
        ENERGIA = "E", "Energia"
        AGUA = "A", "Água"
        MOBILIDADE = "M", "Mobilidade"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.points < 0:
            raise ValueError("Os pontos devem ser um inteiro positivo.")
        return super().save(*args, **kwargs)
