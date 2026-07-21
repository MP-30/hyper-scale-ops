from datetime import time

import pytest
from httpx import AsyncClient

from app.models.classes import Class
from app.models.periods import Period
from app.models.students import Student, StudentDetails
from app.models.teachers import Teacher

pytestmark = pytest.mark.asyncio


async def test_student_and_teacher_form_templates_use_current_api_contract(client: AsyncClient):
    student_form = await client.get("/students/new")
    assert student_form.status_code == 200
    student_html = student_form.text
    assert "/api/v1/new-student" in student_html

    teacher_form = await client.get("/teachers/new")
    assert teacher_form.status_code == 200
    teacher_html = teacher_form.text
    assert 'id="phone_number"' in teacher_html
    assert "/api/v1/teachers/new-teacher" in teacher_html

    period_form = await client.get("/timetable/new")
    assert period_form.status_code == 200
    period_html = period_form.text
    assert "/api/v1/periods/new-period" in period_html
    assert 'id="subject"' not in period_html


async def test_template_pages_render_dynamic_jinja_content(client: AsyncClient, db_session):
    classroom = Class(name="Grade 10", level=10)
    db_session.add(classroom)
    await db_session.flush()

    student_with_class = Student(
        name="Alice Johnson",
        phone_number="1111111111",
        roll_number="R-101",
        class_id=classroom.id,
    )
    student_without_class = Student(
        name="Bob Smith",
        phone_number="2222222222",
        roll_number="R-102",
        class_id=None,
    )
    db_session.add_all([student_with_class, student_without_class])
    await db_session.flush()

    db_session.add_all(
        [
            StudentDetails(
                student_id=student_with_class.id,
                address_line_1="123 Main Street",
                state="Delhi",
                father_name="John Johnson",
            ),
            StudentDetails(
                student_id=student_without_class.id,
                address_line_1="456 Side Street",
                state="Mumbai",
                father_name="Peter Smith",
            ),
        ]
    )

    teacher = Teacher(name="Ms. Rao", phone_number="3333333333", subject="Mathematics")
    db_session.add(teacher)
    await db_session.flush()

    db_session.add(
        Period(
            class_id=classroom.id,
            teacher_id=teacher.id,
            day="monday",
            start_time=time(9, 0),
            end_time=time(10, 0),
        )
    )
    await db_session.commit()

    dashboard_response = await client.get("/")
    assert dashboard_response.status_code == 200
    dashboard_html = dashboard_response.text
    assert "School Insights" in dashboard_html
    assert "Enrolled Students" in dashboard_html
    assert "Active Classes" in dashboard_html
    assert "Total Teachers" in dashboard_html

    students_response = await client.get("/students")
    assert students_response.status_code == 200
    students_html = students_response.text
    assert "Alice Johnson" in students_html
    assert "Bob Smith" in students_html
    assert "Unassigned" in students_html
    assert "Grade 10" in students_html

    teachers_response = await client.get("/teachers")
    assert teachers_response.status_code == 200
    teachers_html = teachers_response.text
    assert "Ms. Rao" in teachers_html
    assert "Mathematics" in teachers_html

    timetable_response = await client.get("/timetable")
    assert timetable_response.status_code == 200
    timetable_html = timetable_response.text
    assert "Monday" in timetable_html
    assert "Mathematics" in timetable_html


async def test_empty_state_templates_render_fallback_messages(client: AsyncClient):
    teachers_response = await client.get("/teachers")
    assert teachers_response.status_code == 200
    assert "No teachers registered yet." in teachers_response.text

    timetable_response = await client.get("/timetable")
    assert timetable_response.status_code == 200
    assert "Timetable matrix is currently empty." in timetable_response.text
