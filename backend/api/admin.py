"""Module admin providing custom django admin objects"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from api.forms import (
    TeamMemberChangeForm, TeamMemberCreationForm
)
from api.models import (
    Team, TeamMember, Happiness
)


class TeamMemberAdmin(UserAdmin):
    """
    Fulfills the admin requirement for custom user model implementation
    """
    form = TeamMemberChangeForm
    add_form = TeamMemberCreationForm
    model = TeamMember

    list_display = (
        'username', 'team', 'is_superuser', 'is_admin', 'is_staff', 'is_active',
    )
    list_filter = (
        'username', 'team', 'is_superuser', 'is_admin', 'is_staff', 'is_active',
    )
    fieldsets = (
        (None, {'fields': (
            'username', 'password',
        )}),
        ('Permissions', {'fields': (
            'is_superuser', 'is_admin', 'is_staff', 'is_active',
        )}),
        ('Custom fields', {'fields': (
            'team',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'team',
            ),
        }),
    )
    search_fields = ('username', 'team',)
    ordering = ('username', 'team',)


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Team)
admin.site.register(Happiness)

# Django's group model is not being used
admin.site.unregister(Group)
