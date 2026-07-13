from django.urls import path
from .views import TaskAPIView, TaskStatusAPIView, TaskCommentAPIView

urlpatterns = [
    path('', TaskAPIView.as_view()),
    path('<int:pk>/', TaskAPIView.as_view()),
    path('<int:pk>/status/', TaskStatusAPIView.as_view()),
    path('<int:pk>/comments/', TaskCommentAPIView.as_view()),
]
