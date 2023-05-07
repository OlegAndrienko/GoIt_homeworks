--Знайти список студентів у певній групі.
SELECT *
FROM students s 
LEFT JOIN groups g ON g.GroupId = s.GroupId 
where s.GroupId = 1