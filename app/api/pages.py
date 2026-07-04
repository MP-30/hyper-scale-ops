from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

pages_router = APIRouter()


@pages_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@pages_router.get("/students")
async def students(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="students.html",
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
    student_id: int
):
    return templates.TemplateResponse(
        request=request,
        name="student_details.html",
        context={
            "student_id": student_id
        }
    )