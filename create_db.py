import sqlite3
from datetime import datetime

from faker import Faker
import faker
from random import randint, choice


START_DATE = datetime(year=2023, month=3, day=1)
END_DATE = datetime(year=2023, month=3, day=30)
STUDENTS_NUMBER = 40
TEACHERS_NUMBER = 5
SUBJECT_NUMBER = 6
GROUP_NUMBER = 3
MARKS_NUMBER = 20

subjects = ["math", "physics", "chemistry", "Ukrainian language", "English", "biology"]
groups = ['Фл-21', 'ФЛ-22', 'ФС-21']


def create_db(sql_name, db_mame):
    # читаємо файл зі скриптом для створення БД
    with open(sql_name, "r") as f:
        sql = f.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect(db_mame) as con:
        cur = con.cursor()
        # виконуємо скрипт із файлу, який створить таблиці в БД
        cur.executescript(sql)


def generate_fake_name(number):
    fake = Faker("uk_UA")
    names_list = []
    names = []
    
    for _ in range(number):
        names_list.append(fake.name())
        
    for name in names_list:
        names.append((name,))
    return names


def generate_fake_date_list(number):
    fake = Faker("uk_UA")
    dates = []
    dates_list = []
    for _ in range(number):
        dates.append.fake.date_between(START_DATE, END_DATE)
    
    for date in dates:
        dates.append((date,))
    return dates


def generate_fake_date():
    fake = Faker("uk_UA")
    date = fake.date_between(START_DATE, END_DATE)
    return date


def generate_group(groups_list):
    groups = []
    
    for group in groups_list:
        groups.append((group,))
    return groups


def prepare_data_for_subjects(subject_list, teacher_number=TEACHERS_NUMBER):
    for_subjects = []
    
    for sub in subject_list:
        for_subjects.append((sub, randint(1, teacher_number)),)
        
    return for_subjects


def prepare_data_for_students(student_tuple_list, group_number = GROUP_NUMBER):
    for_students = []
    
    for st in student_tuple_list:
       st = list(st)
       st.append(randint(1, group_number)) 
       st = tuple(st)
       for_students.append(st)
        
    return for_students


def prepare_data_for_marks(marks_number=MARKS_NUMBER, subject_number= SUBJECT_NUMBER, student_number=STUDENTS_NUMBER):
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
    

def insert_data_to_db(db_mame, teachers, groups, subjects, students, marks):   
    
    
    # create a connect with the db
    with sqlite3.connect(db_mame) as con:
        cur = con.cursor()
        
        sql_to_teachers = """ INSERT INTO teachers(teacher_name)
                                VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)
        
        sql_to_groups = """ INSERT INTO groups(group_name)
                                VALUES (?)"""
        cur.executemany(sql_to_groups, groups)
        
        sql_to_subjects = """ INSERT INTO subjects(subject_name, TeacherId)
                                VALUES (?, ?)"""
        cur.executemany(sql_to_subjects, subjects)
        
        sql_to_students = """ INSERT INTO students(student_name, GroupId)
                                VALUES (?, ?)"""
        cur.executemany(sql_to_students, students)
        
        sql_to_marks = """ INSERT INTO marks(StudentId, SubjectId, mark, mark_date)
                                VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_marks, marks)
        
 
        con.commit()


if __name__ == "__main__":
    sql_name = (
        "C:\\Users\\Oleg\OneDrive\\GOIT_cloud\\bd_module_6\\db_m_6\\db_m_6\\tables.sql"
    )
    
    db_mame = "m6.db"

    create_db(sql_name, db_mame)

    students = generate_fake_name(STUDENTS_NUMBER)
    teachers = generate_fake_name(TEACHERS_NUMBER)
    groups_ins = generate_group(groups) 
    
    subjects_ins = prepare_data_for_subjects(subjects, teacher_number=TEACHERS_NUMBER)
    student_ins = prepare_data_for_students(students, group_number = GROUP_NUMBER)
    marks = prepare_data_for_marks(marks_number=MARKS_NUMBER, subject_number= SUBJECT_NUMBER, student_number=STUDENTS_NUMBER)
    
    insert_data_to_db(db_mame, teachers, groups_ins, subjects_ins, student_ins, marks)
    
