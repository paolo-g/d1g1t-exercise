"""Module permissions providing custom django permissions"""
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission which only allows the access to user's matching the "owner" property
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
