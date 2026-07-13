from django.db import transaction
from .models import Project

@transaction.atomic
def create_project(*, name, description, owner):
    project = Project.objects.create(
        name=name,
        description=description,
        owner=owner
    )
    return project


@transaction.atomic
def archive_project(*, project):
    project.is_archived = True
    project.save(update_fields=['is_archived'])
    return project