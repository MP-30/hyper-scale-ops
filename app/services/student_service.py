from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.students import Student, StudentDetails
from app.schemas.students import StudentCreate, StudentUpdate
from app.exceptions.students import StudentNotFoundException
from app.core.logger import app_logger

class StudentService:
    @staticmethod
    async def get_student(db: AsyncSession, student_id: int):
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.details))
            .filter(Student.id == student_id)
        )
        student = result.scalars().first()

        if student is None:
            raise StudentNotFoundException(student_id)

        return student

    @staticmethod
    async def get_all_students(db: AsyncSession):
        app_logger.info("Fetching all students")
        result = await db.execute(
            select(Student).options(
                selectinload(Student.classroom),
                selectinload(Student.details),
            )
        )
        return result.scalars().all()

    @staticmethod
    async def create_student(
        db: AsyncSession,
        payload: StudentCreate,
    ):
        app_logger.info(f"Creating student '{payload.name}'")

        try:
            student_data = payload.model_dump(exclude={"details"})
            details_data = payload.details.model_dump()
            student = Student(**student_data)
            db.add(student)
            await db.flush()
            student_details = StudentDetails(
                student_id=student.id,
                **details_data,
            )
            db.add(student_details)
            await db.commit()
            app_logger.info(f"Student created successfully. id={student.id}")
            return await StudentService.get_student(
                db,
                student.id,
            )
        except Exception:
            await db.rollback()
            app_logger.exception("Failed to create student")
            raise

    @staticmethod
    async def update_student(
        db: AsyncSession,
        student_id: int,
        payload: StudentUpdate,
    ):
        app_logger.bind(student_id=student_id).info("Updating student")
        student = await StudentService.get_student(
            db,
            student_id,
        )
        try:
            student_data = payload.model_dump(
                exclude={"details"},
                exclude_unset=True,
            )
            for key, value in student_data.items():
                setattr(student, key, value)
            if payload.details:
                details_data = payload.details.model_dump(exclude_unset=True)
                for key, value in details_data.items():
                    setattr(
                        student.details,
                        key,
                        value,
                    )
            await db.commit()
            app_logger.info(f"Student updated successfully. id={student_id}")
            return await StudentService.get_student(
                db,
                student_id,
            )
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed updating student {student_id}")
            raise

    @staticmethod
    async def delete_student(
        db: AsyncSession,
        student_id: int,
    ):
        app_logger.info(f"Deleting student {student_id}")
        student = await StudentService.get_student(
            db,
            student_id,
        )
        try:
            await db.delete(student)
            await db.commit()
            app_logger.info(f"Student deleted successfully. id={student_id}")
        except Exception:
            await db.rollback()
            app_logger.exception(f"Failed deleting student {student_id}")
            raise
