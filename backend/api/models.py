"""Module models providing django models"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.core.validators import (
    MinValueValidator, MaxValueValidator
)
from api.managers import TeamMemberManager

class Team(models.Model):
    """
    Model to store teams
    """
    name = models.CharField(max_length=20,
                            unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.name


class TeamMember(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model so that users can be assigned to a team.
    """
    username = models.CharField(max_length=20,
                                unique=True)
    team = models.ForeignKey(Team,
                             null=True,
                             related_name='user',
                             on_delete=models.SET_NULL)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TeamMemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.username


class Happiness(models.Model):
    """
    Model to store Happiness reports from team members
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='happiness',
                              on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.id)
