-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT teacher_id, COUNT(*) AS num_assignments
FROM Assignments
WHERE grade = 'A'
GROUP BY teacher_id
ORDER BY num_assignments DESC
LIMIT 1;
