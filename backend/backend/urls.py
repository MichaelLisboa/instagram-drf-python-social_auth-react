from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('api.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
