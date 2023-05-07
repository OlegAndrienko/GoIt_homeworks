--Знайти студента із найвищим середнім балом з певного предмета.
SELECT AVG(m.mark) as avg_m, m.SubjectId, s.StudentId, s.student_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
where m.SubjectId = 1
GROUP BY m.SubjectId, m.StudentId 
ORDER BY avg_m  DESC 
LIMIT 1