--Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT AVG(m.mark) as avg_m,   g.group_name
from marks m
LEFT JOIN students s ON m.StudentId = s.StudentId 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
WHERE s.GroupId  = 1
GROUP BY s.GroupId 
ORDER BY avg_m DESC 