""" Module forms providing custom django forms"""
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from api.models import TeamMember

class TeamMemberCreationForm(UserCreationForm):
    """
    Fulfills the user creation form requirement for custom user model implementation
    """
    class Meta:
        """
        Creation fields
        """
        model = TeamMember
        fields = ('username', 'team',)

class TeamMemberChangeForm(UserChangeForm):
    """
    Fulfills the user change form requirement for custom user model implementation
    """
    class Meta:
        """
        Change fields
        """
        model = TeamMember
        fields = ('username', 'team',)
