from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'celebs', views.CelebViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^register-by-token/(?P<backend>[^/]+)/$', views.register_by_access_token)
]
