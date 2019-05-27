from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'celebs', views.CelebViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('convert-token/', views.ConvertToken.as_view(), name='convert_token'),
    path('user/', views.GetUserProfile.as_view()),
]
