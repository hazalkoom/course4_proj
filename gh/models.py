from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.TextField()
    
    def __str__(self):
        return f"profile for {self.user.username}"