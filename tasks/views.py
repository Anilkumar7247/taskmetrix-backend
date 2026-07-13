from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer, TaskCommentSerializer
from .permissions import IsTaskOwnerAssigneeOrAdmin, CanCreateTask
from .services import change_task_status
from .tasks import send_task_notification, send_task_email
from common.redis_client import redis_client
from common.pagination import StandardPagination
from common.rate_limit import rate_limit


class TaskAPIView(APIView):
    """
    List, retrieve, create, update, delete tasks
    """

    def get(self, request, pk=None):
        rate = rate_limit(request)
        if rate:
            return rate

        if pk:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(TaskSerializer(task).data)

        queryset = Task.objects.filter(project__owner=request.user)

        # Filtering
        status_filter = request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TaskSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not CanCreateTask().has_permission(request, self):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(created_by=request.user)
            send_task_notification.delay(task.id)
            if task.assignee:
                send_task_email.delay(task.assignee.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if not IsTaskOwnerAssigneeOrAdmin().has_object_permission(request, self, task):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 'admin':
            return Response({"error": "Only admin can delete tasks"}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatusAPIView(APIView):
    def post(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if not IsTaskOwnerAssigneeOrAdmin().has_object_permission(request, self, task):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        try:
            change_task_status(task=task, new_status=new_status)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        send_task_notification.delay(task.id)
        return Response({"status": task.status})


class TaskCommentAPIView(APIView):
    def post(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

