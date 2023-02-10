from django.urls import include, path
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # API routes
    path('', include('api.urls')),

    # Admin interface (provided by django)
    path('admin/', admin.site.urls),

    # API token creation (provided by rest_framework)
    path('api-token-auth/', obtain_auth_token),
]
