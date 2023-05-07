-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    StudentId INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(50),
    GroupId INTEGER,
    FOREIGN KEY (GroupId) REFERENCES groups(GroupId)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    GroupId INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name VARCHAR(5)
);


-- Table: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    TeacherId INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name VARCHAR(50)
);



-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    SubjectId INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name VARCHAR(50),
    TeacherId INTEGER,
    FOREIGN KEY (TeacherId) REFERENCES teachers(TeacherId)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


-- Table: marks
DROP TABLE IF EXISTS marks;
CREATE TABLE marks (
    StudentId INTEGER,
    SubjectId INTEGER,
    mark INTEGER,
    mark_date DATE,
    FOREIGN KEY (StudentId) REFERENCES students(StudentId)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (SubjectId) REFERENCES subjects(SubjectId)
      ON DELETE CASCADE
      ON UPDATE CASCADE
    
);