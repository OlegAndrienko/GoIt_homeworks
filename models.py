from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

# Таблиця records, де зберігатимуться записи справ для конкретного завдання з таблиці notes 
# - зв'язок one-to-many, поле note_id


#-- Table: groups
class Group(Base):
    __tablename__ = 'groups'
    GroupId = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), nullable=False)
    students = relationship('Student', back_populates= 'group')


# -- Table: students
class Student(Base):
    __tablename__ = 'students'
    StudentId = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(50), nullable=False)
    GroupId = Column(Integer, ForeignKey(Group.GroupId, ondelete="CASCADE", onupdate='CASCADE'))
    group = relationship("Group", back_populates='students')
    mark = relationship("Mark", back_populates='student')
      
    
#-- Table: teachers
class Teacher(Base):
    __tablename__ = 'teachers'
    TeacherId = Column(Integer, primary_key=True, autoincrement=True)
    teacher_name = Column(String(50), nullable=False)
    subjects = relationship('Subject', back_populates='teacher')

# -- Table: subjects
class Subject(Base):
    __tablename__ = 'subjects'
    SubjectId = Column(Integer, primary_key=True, autoincrement=True)
    subject_name =Column(String(50), nullable=False)
    TeacherId = Column(Integer, ForeignKey(Teacher.TeacherId, ondelete="CASCADE", onupdate='CASCADE'))
    teacher = relationship("Teacher", back_populates='subjects')
    mark = relationship('Mark', back_populates='subject')

# -- Table: students
class Mark(Base):
    __tablename__ = 'marks'
    MarkId = Column(Integer, primary_key=True, autoincrement=True)
    StudentId = Column(Integer, ForeignKey(Student.StudentId, ondelete="CASCADE", onupdate='CASCADE'))
    SubjectId = Column(Integer, ForeignKey(Subject.SubjectId, ondelete="CASCADE", onupdate='CASCADE'))
    mark =Column(Integer, nullable=False)
    mark_date = Column(DateTime)
    student = relationship('Student', back_populates='mark')
    subject = relationship('Subject', back_populates= 'mark')
 
 
 
