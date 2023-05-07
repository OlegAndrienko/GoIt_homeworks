--Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT AVG(m.mark) as avg_m, s2.subject_name, t.teacher_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN subjects s2 ON m.SubjectId  = s2.SubjectId 
LEFT JOIN teachers t  ON t.TeacherId  = s2.TeacherId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
WHERE t.TeacherId = 5
GROUP BY t.TeacherId 