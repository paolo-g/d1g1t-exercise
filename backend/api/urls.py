"""Module urls provides django urls"""
from django.urls import path
from api.views.happiness import HappinessViewSet
from api.views.token import token
from api.views.stats import stats

# Happiness model viewset currently supports POSTing only
happiness = HappinessViewSet.as_view({
    'post': 'create'
})

urlpatterns = [
    # Provides a way for users to POST their daily happiness
    path('happiness/',
         happiness,
         name='happiness'),
    # Provides a token invalidation mechanism
    path('token/',
         token,
         name='token'),
    # Provides a team stats report
    path('stats/',
         stats,
         name='stats'),
]
