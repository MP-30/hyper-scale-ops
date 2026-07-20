from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.student_service import StudentService
from app.services.class_service import ClassService

# Assuming standard service layer patterns are built for these two:
from app.services.teacher_service import TeacherService
from app.services.period_service import PeriodService

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

pages_router = APIRouter()

# HOME / DASHBOARD

@pages_router.get("/")
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    # Fetching counts or basic data to make a nice dashboard overview
    students = await StudentService.get_all_students(db)
    classes = await ClassService.get_all_classes(db)
    teachers = await TeacherService.get_all_teachers(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "student_count": len(students),
            "class_count": len(classes),
            "teacher_count": len(teachers),
        },
    )

# STUDENTS PAGES

@pages_router.get("/students")
async def students_page(request: Request, db: AsyncSession = Depends(get_db)):
    students = await StudentService.get_all_students(db)
    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={"students": students},
    )


@pages_router.get("/students/new")
async def new_student_page(request: Request, db: AsyncSession = Depends(get_db)):
    # 💡 Fetch classes so the user can assign the student to a class via a dropdown select
    classes = await ClassService.get_all_classes(db)
    return templates.TemplateResponse(
        request=request, name="student_form.html", context={"classes": classes}
    )


@pages_router.get("/students/{student_id}")
async def student_details_page(
    request: Request, student_id: int, db: AsyncSession = Depends(get_db)
):
    student = await StudentService.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return templates.TemplateResponse(
        request=request,
        name="student_details.html",
        context={"student": student},
    )

# CLASSES PAGES

@pages_router.get("/classes")
async def classes_page(request: Request, db: AsyncSession = Depends(get_db)):
    classes = await ClassService.get_all_classes(db)
    return templates.TemplateResponse(
        request=request,
        name="classes.html",
        context={"classes": classes},
    )


@pages_router.get("/classes/new")
async def new_class_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="class_form.html",
    )


@pages_router.get("/classes/{class_id}")
async def class_details_page(
    request: Request, class_id: int, db: AsyncSession = Depends(get_db)
):
    classroom = await ClassService.get_class(db, class_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Class not found")

    return templates.TemplateResponse(
        request=request,
        name="class_details.html",
        context={"classroom": classroom},
    )
# TEACHERS PAGES

@pages_router.get("/teachers")
async def teachers_page(request: Request, db: AsyncSession = Depends(get_db)):
    teachers = await TeacherService.get_all_teachers(db)
    return templates.TemplateResponse(
        request=request,
        name="teachers.html",
        context={"teachers": teachers},
    )


@pages_router.get("/teachers/new")
async def new_teacher_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="teacher_form.html",
    )


@pages_router.get("/teachers/{teacher_id}")
async def teacher_details_page(
    request: Request, teacher_id: int, db: AsyncSession = Depends(get_db)
):
    teacher = await TeacherService.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return templates.TemplateResponse(
        request=request,
        name="teacher_details.html",
        context={"teacher": teacher},
    )



# TIMETABLE / PERIODS PAGES



@pages_router.get("/timetable")
async def timetable_page(request: Request, db: AsyncSession = Depends(get_db)):
    periods = await PeriodService.get_all_periods(db)
    return templates.TemplateResponse(
        request=request,
        name="timetable.html",
        context={"periods": periods},
    )


@pages_router.get("/timetable/new")
async def new_period_page(request: Request, db: AsyncSession = Depends(get_db)):
    # 💡 A new period setup needs dropdown elements for both classes and teachers!
    classes = await ClassService.get_all_classes(db)
    teachers = await TeacherService.get_all_teachers(db)

    return templates.TemplateResponse(
        request=request,
        name="period_form.html",
        context={"classes": classes, "teachers": teachers},
    )
