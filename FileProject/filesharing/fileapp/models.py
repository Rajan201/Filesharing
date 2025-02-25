from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    share_link = models.CharField(max_length=100, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.share_link:
            self.share_link = get_random_string(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
