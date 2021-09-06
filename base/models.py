from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # username
    title = models.CharField(max_length=200)  # title of item
    description = models.TextField(null=True, blank=True)  # description
    complete = models.BooleanField(default=False)  # status of item
    create = models.DateTimeField(auto_now_add=True)  # time of creation

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
