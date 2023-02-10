""" Module happiness providing happiness endpoints"""
from datetime import date
from rest_framework import (
    status, viewsets
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Happiness
from api.permissions import IsOwner
from api.serializers import HappinessSerializer

class HappinessViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """
    API endpoints that allows users to POST their happiness level once per day
    """
    queryset = Happiness.objects.all()
    serializer_class = HappinessSerializer
    permission_classes = [IsAuthenticated,
                          IsOwner]

    def create(self, request, *args, **kwargs):
        """
        Overrides the ModelViewSet's default create()
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Make sure this user doesn't already have a happiness report for today
        try:
            Happiness.objects.get(owner=self.request.user,
                                  created_at__gte=date.today())

            # No exception thrown; a happiness report already exists for this user today
            errors = {'errors': 'Happiness report already exists for this user today.'}
            return Response(errors, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except Happiness.DoesNotExist:
            # No happiness report found; create one
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Overrides the ModelViewSet's default perform_create()
        """
        # Force the owner of the report to the current user
        serializer.save(owner=self.request.user)
