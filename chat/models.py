from django.db import models
from django.contrib.auth.models import AbstractUser

# First define Role without using User
class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.JSONField(blank=True, null=True)
    hierarchy_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Now define User and link to Role
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

# Now it's safe to define Message and link both Role and User
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    visible_to_roles = models.ManyToManyField(Role, blank=True)
    visible_to_users = models.ManyToManyField(User, related_name='visible_messages', blank=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"


