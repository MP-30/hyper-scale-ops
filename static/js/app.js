// ================================
// Load All Students
// ================================
async function loadStudents() {

    const tableBody = document.querySelector("#students-table tbody");

    // Not on students page
    if (!tableBody) {
        return;
    }

    try {

        const response = await fetch("/api/v1/all-students");

        if (!response.ok) {
            throw new Error("Unable to fetch students.");
        }

        const students = await response.json();

        tableBody.innerHTML = "";

        students.forEach(student => {

            tableBody.innerHTML += `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.phone_number}</td>
                    <td>${student.roll_number}</td>
                    <td>${student.grade}</td>

                    <td>
                        <a href="/students/${student.id}">👁 View</a>
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Failed to load students.
                </td>
            </tr>
        `;

    }

}

// ================================
// Create Student
// ================================
async function createStudent(event) {

    event.preventDefault();

    const payload = {

        name: document.getElementById("name").value,

        phone_number: document.getElementById("phone_number").value,

        roll_number: document.getElementById("roll_number").value,

        grade: document.getElementById("grade").value,

        details: {

            address_line_1: document.getElementById("address_line_1").value,

            address_line_2: document.getElementById("address_line_2").value,

            state: document.getElementById("state").value,

            father_name: document.getElementById("father_name").value

        }

    };

    try {

        const response = await fetch("/api/v1/new-student", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)

        });

        if (response.ok) {

            alert("Student created successfully!");

            window.location.href = "/students";

        } else {

            const error = await response.json();

            console.error(error);

            alert(JSON.stringify(error, null, 2));

        }

    } catch (error) {

        console.error(error);

        alert("Something went wrong.");

    }

}

// ================================
// Register Form Event
// ================================
const studentForm = document.getElementById("student-form");

if (studentForm) {
    studentForm.addEventListener("submit", createStudent);
}

// ================================
// Initialize
// ================================
loadStudents();