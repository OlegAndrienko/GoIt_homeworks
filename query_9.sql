--Знайти список курсів, які відвідує студент.
SELECT  s2.subject_name, s.student_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN subjects s2 ON m.SubjectId  = s2.SubjectId 
LEFT JOIN teachers t  ON t.TeacherId  = s2.TeacherId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
where s.StudentId = 30