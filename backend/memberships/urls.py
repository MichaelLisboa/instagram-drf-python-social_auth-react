from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'products', views.MembershipsViewSet)
router.register(r'users', views.UserMembershipsViewSet)
router.register(r'subscriptions', views.SubscriptionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscription/<int:pk>/', views.SocialSubscription.as_view()),
]
