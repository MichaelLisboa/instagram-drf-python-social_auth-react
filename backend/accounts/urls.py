from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'influencer', views.CelebViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('convert-token/', views.ConvertToken.as_view(), name='convert_token'),
    path('u/', views.GetUserProfile.as_view()),
    path('update-email/<int:pk>/', views.UpdateEmail.as_view()),

    re_path(
            r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.ActivateEmail.as_view(),
            name='activate'
            ),
]
