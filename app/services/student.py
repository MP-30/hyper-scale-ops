from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession
from app.models.students import Student, StudentDetails
from app.schemas import students
from app.schemas.students import StudentCreate, StudentUpdate
from sqlalchemy.orm import selectinload

class StudentService:

    @staticmethod
    async def create_student(
            db: AsyncSession,
            payload: StudentCreate
    ):
        student = Student(
            name= payload.name,
            phone_number= payload.phone_number,
            roll_number  = payload.roll_number,
            grade= payload.grade
        )

        student.details = StudentDetails(
            address_line_1= payload.details.address_line_1,
            address_line_2= payload.details.address_line_2,
            state = payload.details.state,
            father_name= payload.details.father_name
        )

        db.add(student)
        await db.commit()
        await db.refresh(student,["details"])

        return student

    @staticmethod
    async def get_all_students(
            db: AsyncSession,
    ):
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.details))
        )
        students = result.scalars().all()
        return students

    @staticmethod
    async  def get_student(
            db: AsyncSession,
            students_id:int
    ):
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.details))
            .where(Student.id == students_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_student(
        db: AsyncSession,
        student_id: int,
        payload: StudentUpdate
    ):
        student = await StudentService.get_student(
            db,
            student_id
        )

        if not student:
            return None

        update_data = payload.model_dump(
            exclude_unset=True
        )
        for key, value in update_data.items():
            setattr(student, key, value)

        await db.commit()

        return await StudentService.get_student(
            db,
            student_id,
        )

    @staticmethod
    async def delete_student(
            db: AsyncSession,
            student_id: int
    ):
        student = await StudentService.get_student(
            db,
            student_id
        )
        if not student:
            return False

        await db.delete(student)
        await db.commit()

        return True
