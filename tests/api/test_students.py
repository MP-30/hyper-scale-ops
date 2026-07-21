import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_student_complete_crud_lifecycle(client: AsyncClient):
    """
    Tests the full student CRUD lifecycle:
    Create -> Read All -> Read One -> Update -> Delete -> Verify 404
    """

    # 1. CREATE
    new_student_payload = {
        "name": "Aditya Kumar",
        "phone_number": "9876543210",
        "roll_number": "CS-101",
        "class_id": None,  # Match our schema (uses class_id instead of grade)
        "details": {
            "address_line_1": "123 MG Road",
            "address_line_2": "Near Railway Station",
            "state": "Madhya Pradesh",
            "father_name": "Rajesh Kumar",
        },
    }

    create_response = await client.post(
        "/api/v1/new-student",
        json=new_student_payload,
    )

    assert create_response.status_code == 201, f"Failed to create student: {create_response.text}"
    student_data = create_response.json()

    assert "id" in student_data
    assert student_data["name"] == "Aditya Kumar"
    assert student_data["phone_number"] == "9876543210"
    assert student_data["roll_number"] == "CS-101"
    assert student_data["class_id"] is None

    assert student_data["details"]["address_line_1"] == "123 MG Road"
    assert student_data["details"]["state"] == "Madhya Pradesh"
    assert student_data["details"]["father_name"] == "Rajesh Kumar"

    student_id = student_data["id"]

    # 2. READ ALL
    all_response = await client.get("/api/v1/all-students")
    assert all_response.status_code == 200
    all_students = all_response.json()

    assert len(all_students) >= 1
    assert any(student["id"] == student_id for student in all_students)

    # 3. READ ONE
    fetch_response = await client.get(f"/api/v1/fetch-one-student/{student_id}")
    assert fetch_response.status_code == 200
    fetched_student = fetch_response.json()

    assert fetched_student["id"] == student_id
    assert fetched_student["name"] == "Aditya Kumar"
    assert fetched_student["roll_number"] == "CS-101"

    # 4. UPDATE
    update_payload = {
        "name": "Aditya Shrivastava",
        "phone_number": "9999999999"
    }

    update_response = await client.put(
        f"/api/v1/modify-student/{student_id}",
        json=update_payload,
    )

    assert update_response.status_code == 200
    updated_student = update_response.json()

    assert updated_student["id"] == student_id
    assert updated_student["name"] == "Aditya Shrivastava"
    assert updated_student["phone_number"] == "9999999999"
    assert updated_student["roll_number"] == "CS-101"  # Retained old value safely

    # 5. DELETE
    delete_response = await client.delete(f"/api/v1/delete-student/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Student record deleted successfully"  # Matches router exact message
    }

    # 6. VERIFY DELETED
    deleted_response = await client.get(f"/api/v1/fetch-one-student/{student_id}")
    assert deleted_response.status_code == 404
    assert deleted_response.json()["detail"] == "Student record not found" # Matches router exact error


async def test_fetch_student_not_found(client: AsyncClient):
    """Verify fetching a non-existent student returns 404."""
    response = await client.get("/api/v1/fetch-one-student/99999")
    assert response.status_code == 404
    body = response.json()

    assert body["success"] is False
    assert body["error"]["code"] == "STUDENT_NOT_FOUND"
    assert body["error"]["message"] == "Student record not found."


async def test_modify_student_not_found(client: AsyncClient):
    """Verify updating a non-existent student returns 404."""
    payload = {
        "name": "Ghost",
        "phone_number": "9999999999"
    }
    response = await client.put("/api/v1/modify-student/99999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student record not found"


async def test_delete_student_not_found(client: AsyncClient):
    """Verify deleting a non-existent student returns 404."""
    response = await client.delete("/api/v1/delete-student/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student record not found"