--Знайти 5 студентів із найбільшим середнім балом з усіх предметів
SELECT AVG(m.mark) as avg_m, m.StudentId, s.student_name 
from marks m 
LEFT JOIN students s ON m.StudentId = s.StudentId 
GROUP BY m.StudentId
ORDER BY avg_m DESC 
LIMIT 5
