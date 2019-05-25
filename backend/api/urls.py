from django.urls import include, path, re_path

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('memberships/', include('memberships.urls')),
]
