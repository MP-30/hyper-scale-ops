from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.students import Student, StudentDetails
from app.schemas.students import StudentCreate, StudentUpdate


class StudentService:
    @staticmethod
    async def get_student(db: AsyncSession, student_id: int):
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.details))
            .filter(Student.id == student_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all_students(db: AsyncSession):
        result = await db.execute(
            select(Student).options(
                selectinload(Student.classroom),
                selectinload(Student.details),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def create_student(db: AsyncSession, payload: StudentCreate):
        # 1. Extract details data out of the main payload
        student_data = payload.model_dump(exclude={"details"})
        details_data = payload.details.model_dump()

        # 2. Build and save the core student row
        student = Student(**student_data)
        db.add(student)
        await db.flush()  # Flushes to get the new student.id without committing yet

        # 3. Build and save details tied to that student ID
        student_details = StudentDetails(student_id=student.id, **details_data)
        db.add(student_details)

        await db.commit()

        # 4. Safely return fully loaded model bundle
        return await StudentService.get_student(db, student.id)

    @staticmethod
    async def update_student(db: AsyncSession, student_id: int, payload: StudentUpdate):
        student = await StudentService.get_student(db, student_id)
        if not student:
            return None

        # Update core student fields if provided
        student_data = payload.model_dump(exclude={"details"}, exclude_unset=True)
        for key, value in student_data.items():
            setattr(student, key, value)

        # Update nested details table if provided
        if payload.details:
            details_data = payload.details.model_dump(exclude_unset=True)
            for key, value in details_data.items():
                setattr(student.details, key, value)

        await db.commit()
        return await StudentService.get_student(db, student_id)

    @staticmethod
    async def delete_student(db: AsyncSession, student_id: int):
        student = await StudentService.get_student(db, student_id)
        if not student:
            return False

        await db.delete(
            student
        )  # If cascade is set, details table clears automatically
        await db.commit()
        return True
