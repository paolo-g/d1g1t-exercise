""" Module logout providing logout endpoints"""
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['DELETE'])
def token(request):
    """
    API GET endpoint that deletes the user's api token
    """
    Token.objects.get(key=request.user.auth_token).delete()
    return Response({}, status=status.HTTP_200_OK)
