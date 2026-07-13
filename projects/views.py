from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsProjectOwnerOrAdmin, CanCreateProject
from .services import create_project, archive_project


class ProjectAPIView(APIView):
    """
    API view to list, retrieve, create, update, or delete projects.
    """

    def get(self, request, pk=None):
        try:
            if pk:
                project = Project.objects.get(pk=pk, is_archived=False)
                serializer = ProjectSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)

            projects = Project.objects.filter(owner=request.user, is_archived=False)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        permission = CanCreateProject()
        if not permission.has_permission(request, self):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = create_project(
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', ''),
                owner=request.user
            )
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        project = Project.objects.filter(pk=pk, is_archived=False).first()
        if not project:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        permission = IsProjectOwnerOrAdmin()
        if not permission.has_object_permission(request, self, project):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        project = Project.objects.filter(pk=pk, is_archived=False).first()
        if not project:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        permission = IsProjectOwnerOrAdmin()
        if not permission.has_object_permission(request, self, project):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        archive_project(project=project)
        return Response({"message": "Project archived successfully"}, status=status.HTTP_200_OK)
