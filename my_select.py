from connect_db import session
from models import Group, Student, Teacher, Subject, Mark
from sqlalchemy import select, update, delete, values
from sqlalchemy.sql import func, desc, cast

import sqlite3
from datetime import datetime

from faker import Faker
import faker
from random import randint


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    stmt = (
        session.query(
            Student.student_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Student)
        .group_by(Student.StudentId)
        .order_by(desc("average_mark"))
        .limit(5)
        .all()
    )
    return stmt

#найти студента із найвищим середнім балом з певного предмета.
def select_2(sub_id=2):
    stmt = (
        session.query(
            Student.student_name,
            Subject.SubjectId,
            Subject.subject_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .where(Mark.SubjectId == sub_id)
        .group_by(Student.StudentId)
        .order_by(desc("average_mark"))
        .limit(1)
        .all()
    )
    return stmt

#Знайти середній бал у групах з певного предмета
def select_3(sub_id=2):
    stmt = (
        session.query(
            Group.group_name,
            Subject.SubjectId,
            Subject.subject_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .join(Subject)
        .where(Mark.SubjectId == sub_id)
        .group_by(Group.GroupId)
        .order_by(desc("average_mark"))
        .all()
    )
    return stmt

#-Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    stmt = (
        session.query(
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
         .all()
    )
    return stmt

#--Знайти які курси читає певний викладач.
def select_5(teach_id=2):
    stmt = (
        session.query(
            Subject.SubjectId,
            Subject.subject_name,
            Teacher.teacher_name,
        )
        .select_from(Subject)
        .join(Teacher)
        .where(Teacher.TeacherId == teach_id)
        .group_by(Teacher.teacher_name)
        # .order_by(desc("average_mark"))
        # .limit(5)
        .all()
    )
    return stmt

#Знайти список студентів у певній групі.
def select_6(group_id=1):
    stmt = (
        session.query(
            Student.StudentId,
            Student.student_name,
            Group.group_name
        )
        .select_from(Student)
        .join(Group)
        .where(Group.GroupId == group_id)
        .all()
    )
    return stmt

#Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id=1, sub_id=2):
    stmt = (
        session.query(
            Subject.subject_name,
            Mark.mark,
            Student.student_name,
            Group.group_name
        )
        .select_from(Mark)
        .join(Student)
        .join(Subject).filter(Subject.SubjectId == sub_id)
        .join(Group).filter(Group.GroupId == group_id)
        # .where(Group.GroupId == group_id and Subject.SubjectId == sub_id)
        .all()
    )
    return stmt

#Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teach_id=2):
    stmt = (
        session.query(
            Teacher.teacher_name,
            Subject.subject_name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .select_from(Mark)
        .group_by(Teacher.teacher_name)
        .where(Teacher.TeacherId == teach_id)
        .all()
    )
    return stmt

#Знайти список курсів, які відвідує студент.
def select_9(student_id=30):
    stmt = (
        session.query(
            Subject.subject_name,
        )
        .select_from(Mark)
        .join(Student).filter(Student.StudentId == student_id)
        # .join(Subject).filter(Subject.SubjectId == sub_id)
        # .join(Group).filter(Group.GroupId == group_id)
        # .where(Group.GroupId == group_id and Subject.SubjectId == sub_id)
        .all()
    )
    return stmt

#Список курсів, які певному студенту читає певний викладач.
def select_10(student_id=30, teach_id =2):
    stmt = (
        session.query(
            Subject.subject_name,
            Student.student_name
        )
        .select_from(Mark)
        .join(Student).filter(Student.StudentId == student_id)
        .where(Teacher.TeacherId == teach_id)
        .all()
    )
    return stmt


print(select_1())
print(select_2())
print(select_3())
print(select_4())
print(select_5())
print(select_6())
print(select_7())
print(select_8())
print(select_9())
print(select_10())



