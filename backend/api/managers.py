"""Module managers provides CustomUser managers"""
from django.contrib.auth.models import BaseUserManager

class TeamMemberManager(BaseUserManager):
    """
    A user manager for the custom user model
    """
    def create_user(self, username, password=None, **properties):
        """
        Creates a user

        :param username: The unique username
        :param password: User password
        :param properties: Grouping of other user properties
        :return User:
        """
        if not username:
            raise ValueError('User requires a username')

        user = self.model(
            username=username,
            **properties
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **properties):
        """
        Creates a superuser

        :param username: The unique username
        :param password: User password
        :param properties: Grouping of other user properties
        :return User:
        """
        properties['is_superuser'] = True
        properties['is_admin'] = True
        properties['is_staff'] = True

        return self.create_user(username, password, **properties)
