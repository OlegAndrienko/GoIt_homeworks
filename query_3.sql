--Знайти середній бал у групах з певного предмета.
SELECT AVG(m.mark) as avg_m, m.SubjectId, m.StudentId,  g.group_name, s.student_name 
from marks m
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
WHERE m.SubjectId = 1
GROUP BY s.GroupId 
ORDER BY avg_m DESC 