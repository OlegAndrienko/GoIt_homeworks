--Список курсів, які певному студенту читає певний викладач.
SELECT  s2.subject_name, s.student_name, t.teacher_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN subjects s2 ON m.SubjectId  = s2.SubjectId 
LEFT JOIN teachers t  ON t.TeacherId  = s2.TeacherId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
where s.StudentId = 3 and t.TeacherId = 5