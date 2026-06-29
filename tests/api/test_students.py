import pytest
from httpx import AsyncClient

# Tell pytest-asyncio to automatically treat all tests in this file as async
pytestmark = pytest.mark.asyncio


async def test_student_complete_crud_lifecycle(client: AsyncClient):
    """
    Tests the full end-to-end lifecycle of a student record:
    Create -> Read All -> Read One -> Update -> Delete -> 404 Verification.
    """

    # -------------------------------------------------------------
    # 1. CREATE: Test POST /new-student
    # -------------------------------------------------------------
    new_student_payload = {
        "name": "Aditya Kumar",
        "phone_number": "9876543210",
        "roll_number": "CS-101",
        "grade": "A",
        "details": {
            "address_line_1": "123 MG Road",
            "address_line_2": "Near Railway Station",
            "state": "Madhya Pradesh",
            "father_name": "Rajesh Kumar"
        }
    }

    create_response = await client.post("/api/v1/new-student", json=new_student_payload)
    assert create_response.status_code == 201, f"Failed to create: {create_response.text}"

    student_data = create_response.json()
    assert student_data["name"] == "Aditya Kumar"
    assert student_data["email"] == "aditya.ops@example.com"
    assert "id" in student_data

    student_id = student_data["id"]

    # -------------------------------------------------------------
    # 2. READ ALL: Test GET /all-students
    # -------------------------------------------------------------
    all_response = await client.get("/api/v1/all-students")
    assert all_response.status_code == 200

    all_students = all_response.json()
    assert len(all_students) >= 1
    # Verify our newly created student is present in the database array
    assert any(s["id"] == student_id for s in all_students)

    # -------------------------------------------------------------
    # 3. READ ONE: Test GET /fetch-one-student/{student_id}
    # -------------------------------------------------------------
    fetch_response = await client.get(f"/api/v1/fetch-one-student/{student_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["name"] == "Aditya Kumar"

    # -------------------------------------------------------------
    # 4. UPDATE: Test PUT /modify-student/{student_id}
    # -------------------------------------------------------------
    update_payload = {
        "name": "Aditya Shrivastava",
        "phone_number": "9999999999",
        "grade": "A+"
    }

    update_response = await client.put(f"/api/v1/modify-student/{student_id}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Aditya Shrivastava"
    assert update_response.json()["age"] == 25

    # -------------------------------------------------------------
    # 5. DELETE: Test DELETE /delete-student/{student_id}
    # -------------------------------------------------------------
    delete_response = await client.delete(f"/api/v1/delete-student/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Student deleted successfully"

    # -------------------------------------------------------------
    # 6. VERIFY 404: Ensure the deleted student no longer exists
    # -------------------------------------------------------------
    get_deleted_response = await client.get(f"/api/v1/fetch-one-student/{student_id}")
    assert get_deleted_response.status_code == 404
    assert get_deleted_response.json()["detail"] == "Student not found"


async def test_fetch_student_not_found(client: AsyncClient):
    """Verifies 404 exception paths for non-existent IDs."""
    response = await client.get("/api/v1/fetch-one-student/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


async def test_modify_student_not_found(client: AsyncClient):
    """Verifies 404 exception paths when updating a non-existent student."""
    invalid_payload = {
        "name": "Ghost",
        "email": "ghost@example.com",
        "age": 30
    }
    response = await client.put("/api/v1/modify-student/99999", json=invalid_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


async def test_delete_student_not_found(client: AsyncClient):
    """Verifies 404 exception paths when deleting a non-existent student."""
    response = await client.delete("/api/v1/delete-student/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
