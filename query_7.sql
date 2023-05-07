--Знайти оцінки студентів у окремій групі з певного предмета.
SELECT m.mark, s2.subject_name, s.student_name, g.group_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN subjects s2 ON m.SubjectId  = s2.SubjectId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
where g.GroupId = 1 AND s2.SubjectId = 3