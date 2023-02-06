from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='Users')
router.register('santaUsers', views.SantaUserViewSet, basename='SantaUsers')
router.register('santaGroups', views.SantaGroupViewSet, basename='SantaGroups')
router.register('santaLists', views.SantaListViewSet, basename='SantaLists')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
