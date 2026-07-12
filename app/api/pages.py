from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.student import StudentService

BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")

pages_router = APIRouter()


@pages_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@pages_router.get("/students")
async def students(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    students = await StudentService.get_all_students(db)

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "students": students
        },
    )


@pages_router.get("/students/new")
async def new_student(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="student_form.html",
    )


@pages_router.get("/students/{student_id}")
async def student_details(
    request: Request,
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    student = await StudentService.get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="student_details.html",
        context={
            "student": student
        },
    )