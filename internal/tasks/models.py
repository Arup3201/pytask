from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=256)
    display_name = models.CharField(max_length=64)
    password_hash = models.BinaryField("Password hash bytes")

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    is_completed = models.BooleanField("Task has been completed or not")

