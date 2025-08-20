from app.database.base import Base

from app.models.role import Role
from app.models.user import User
from app.models.class_ import Class, StudentClass
from app.models.relations import ParentStudent, TeacherSubjectClass
from app.models.subject import Subject
from app.models.classroom import Classroom
from app.models.academic_period import AcademicPeriod
from app.models.lesson import Lesson
from app.models.attendance import Attendance
from app.models.grade import Grade, FinalGrade
from app.models.homework import Homework, HomeworkSubmission
from app.models.substitution import Substitution
from app.models.notification import Notification
