--Знайти які курси читає певний викладач.
SELECT *
FROM subjects s 
LEFT JOIN teachers t ON t.TeacherId  = s.TeacherId 
WHERE s.TeacherId = 1