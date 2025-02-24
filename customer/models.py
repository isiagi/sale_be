from django.db import models
from users.models import CustomUser as User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
