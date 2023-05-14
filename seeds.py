from connect_db import session
from models import Group, Student, Teacher, Subject, Mark
from sqlalchemy import select, update, delete, values

import sqlite3
from datetime import datetime

from faker import Faker
import faker
from random import randint


START_DATE = datetime(year=2023, month=3, day=1)
END_DATE = datetime(year=2023, month=3, day=30)
STUDENTS_NUMBER = 40
TEACHERS_NUMBER = 5
SUBJECT_NUMBER = 6
GROUP_NUMBER = 3
MARKS_NUMBER = 20

subjects = ["math", "physics", "chemistry", "Ukrainian language", "English", "biology"]
groups = ["ФЛ-21", "ФЛ-22", "ФС-21"]


def generate_fake_name(number):
    fake = Faker("uk_UA")
    names_list = []

    for _ in range(number):
        names_list.append(fake.name())

    return names_list


def generate_fake_date_list(number):
    fake = Faker("uk_UA")
    dates = []
    dates_list = []

    for _ in range(number):
        fake_date = fake.date_between(START_DATE, END_DATE)
        dates.append(fake_date)

    return dates


def generate_fake_date(start=START_DATE, end=END_DATE):
    fake = Faker("uk_UA")
    date = fake.date_between(start, end)
    return date


def generate_group(groups_list):
    groups = []

    for group in groups_list:
        groups.append((group,))
    return groups


def prepare_data_for_subjects(subject_list, teacher_number=TEACHERS_NUMBER):
    for_subjects = []

    for sub in subject_list:
        for_subjects.append(
            (sub, randint(1, teacher_number)),
        )

    return for_subjects


def prepare_data_for_students(student_tuple_list, group_number=GROUP_NUMBER):
    for_students = []

    for st in student_tuple_list:
        st = list(st)
        st.append(randint(1, group_number))
        st = tuple(st)
        for_students.append(st)

    return for_students


def prepare_data_for_marks(
    marks_number=MARKS_NUMBER,
    subject_number=SUBJECT_NUMBER,
    student_number=STUDENTS_NUMBER,
):
    for_marks = []
    record = ()

    for st_id in range(1, student_number):
        for j in range(1, marks_number):
            sub_id = randint(1, subject_number)
            mark = randint(3, 5)
            date = generate_fake_date()
            record = (st_id, sub_id, mark, date)
            for_marks.append(record)
    return for_marks


def table_delete_before_update(Object):
    row_number = session.query(Object).count()

    if row_number > 0:
        for i in range(1, row_number + 1):
            row_delete = session.get(Object, i)
            session.delete(row_delete)
            session.commit()


def group_add_all(group_list):
    group_insts = []

    for group in group_list:
        group_inst = Group(group_name=group)
        group_insts.append(group_inst)

    session.add_all(group_insts)
    session.commit()


def teacher_add_all(teacher_list, Table_object):
    table_insts = []

    for teacher in teacher_list:
        table_inst = Table_object(teacher_name=teacher)
        table_insts.append(table_inst)

    session.add_all(table_insts)
    session.commit()


def student_add_all(student_list, Table_object, group_number=GROUP_NUMBER):
    table_insts = []

    for student in student_list:
        group_number = randint(1, group_number)
        table_inst = Table_object(student_name=student, GroupId=group_number)
        table_insts.append(table_inst)

    session.add_all(table_insts)
    session.commit()


def subject_add_all(subject_list, Table_object, teachers_number=TEACHERS_NUMBER):
    table_insts = []

    for subject in subject_list:
        teacher_number = randint(1, teachers_number)
        table_inst = Table_object(subject_name=subject, TeacherId=teacher_number)
        table_insts.append(table_inst)

    session.add_all(table_insts)
    session.commit()


def mark_add_all(
    Table_object,
    marks_number=MARKS_NUMBER,
    subject_number=SUBJECT_NUMBER,
    student_number=STUDENTS_NUMBER,
):
    for_marks = []
    record = []

    for st_id in range(1, student_number + 1):
        for j in range(1, marks_number + 1):
            sub_id = randint(1, subject_number)
            mark = randint(3, 5)
            date = generate_fake_date()
            record = Table_object(
                StudentId=st_id, SubjectId=sub_id, mark=mark, mark_date=date
            )
            for_marks.append(record)

    session.add_all(for_marks)
    session.commit()


if __name__ == "__main__":
    # insert Group
    table_delete_before_update(Group)
    group_add_all(groups)

    # insert Teacher
    teacher_list = generate_fake_name(TEACHERS_NUMBER)
    table_delete_before_update(Teacher)
    teacher_add_all(teacher_list, Teacher)

    # insert Student
    student_list = generate_fake_name(STUDENTS_NUMBER)
    table_delete_before_update(Student)
    student_add_all(student_list, Student)

    # insert Subject
    table_delete_before_update(Subject)
    subject_add_all(subjects, Subject, teachers_number=TEACHERS_NUMBER)

    # insert Mark
    table_delete_before_update(Mark)
    mark_add_all(
        Mark,
        marks_number=MARKS_NUMBER,
        subject_number=SUBJECT_NUMBER,
        student_number=STUDENTS_NUMBER,
    )
   
