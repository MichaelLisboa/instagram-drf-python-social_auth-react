from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'celebs', views.CelebViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
