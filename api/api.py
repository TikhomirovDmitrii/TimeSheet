from datetime import date
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router, Schema
from ninja.security import HttpBearer
from pydantic import BaseModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .models import Project, User, WorkLog

api = NinjaAPI(title="Timesheet API")


class ProjectSchema(BaseModel):
    name: str
    description: str = ""


class WorkLogSchema(BaseModel):
    user_id: int
    project_id: int
    hours: float
    date: date


class ReportItemSchema(Schema):
    id: int
    hours: float


class ReportSchema(Schema):
    data: List[ReportItemSchema]


router = Router()


@router.get("/projects/", response=List[ProjectSchema])
def list_projects(request):
    """Получить список всех проектов"""
    return list(Project.objects.all().values("name", "description"))


@router.post("/projects/")
def create_project(request, payload: ProjectSchema):
    """Создать новый проект"""
    project = Project.objects.create(**payload.model_dump())
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
    }


@router.get("/projects/{project_id}/", response=ProjectSchema)
def get_project(request, project_id: int):
    """Получить информацию о проекте"""
    project = get_object_or_404(Project, id=project_id)
    return {"name": project.name, "description": project.description}


@router.put("/projects/{project_id}/")
def update_project(request, project_id: int, payload: ProjectSchema):
    """Обновить проект"""
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.model_dump().items():
        setattr(project, attr, value)
    project.save()
    return {"success": True}


@router.delete("/projects/{project_id}/")
def delete_project(request, project_id: int):
    """Удалить проект"""
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True}


@router.get("/worklogs/", response=List[WorkLogSchema])
def list_worklogs(request):
    """Получить список всех записей о рабочем времени"""
    return list(
        WorkLog.objects.all().values("user_id", "project_id", "hours", "date")
    )


@router.post("/worklogs/")
def create_worklog(request, payload: WorkLogSchema):
    """Создать запись о рабочем времени"""
    try:
        user = User.objects.get(id=payload.user_id)
        project = Project.objects.get(id=payload.project_id)
    except ObjectDoesNotExist:
        raise Http404("Пользователь или проект не найдены")

    worklog = WorkLog.objects.create(
        user=user,
        project=project,
        hours=payload.hours,
        date=payload.date,
    )
    return {
        "id": worklog.id,
        "user_id": worklog.user.id,
        "project_id": worklog.project.id,
        "hours": worklog.hours,
        "date": worklog.date,
    }


@router.get("/worklogs/{worklog_id}/", response=WorkLogSchema)
def get_worklog(request, worklog_id: int):
    """Получить информацию о конкретной записи"""
    worklog = get_object_or_404(WorkLog, id=worklog_id)
    return {
        "user_id": worklog.user.id,
        "project_id": worklog.project.id,
        "hours": worklog.hours,
        "date": worklog.date,
    }


@router.put("/worklogs/{worklog_id}/")
def update_worklog(request, worklog_id: int, payload: WorkLogSchema):
    """Обновить запись о рабочем времени"""
    worklog = get_object_or_404(WorkLog, id=worklog_id)
    for attr, value in payload.model_dump().items():
        setattr(worklog, attr, value)
    worklog.save()
    return {"success": True}


@router.delete("/worklogs/{worklog_id}/")
def delete_worklog(request, worklog_id: int):
    """Удалить запись о рабочем времени"""
    worklog = get_object_or_404(WorkLog, id=worklog_id)
    worklog.delete()
    return {"success": True}


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError):
            return None


@router.get(
    "/reports/{project_id}/",
    response=List[ReportItemSchema],
    auth=JWTAuth(),
)
def get_report(request, project_id: int, start_date: date, end_date: date):
    """Генерация отчёта по проекту (по каждому пользователю)"""
    worklogs = (
        WorkLog.objects.filter(
            project_id=project_id,
            date__gte=start_date,
            date__lt=end_date,
        )
        .values("user__id")
        .annotate(total_hours=models.Sum("hours"))
    )

    result = [
        {"id": log["user__id"], "hours": float(log["total_hours"])}
        for log in worklogs
    ]

    return result


api.add_router("/", router)
