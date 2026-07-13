from django.urls import path
from .views import ( ProfileAPIView, UserListAPIView, UserDetailAPIView,)

urlpatterns = [
    path('profile/', ProfileAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
]