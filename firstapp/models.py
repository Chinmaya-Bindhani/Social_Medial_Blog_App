from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField(max_length=100)
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table='post'

    def get_absolute_url(self):
        return reverse('home')