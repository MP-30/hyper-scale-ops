import pytest
from httpx import AsyncClient

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
