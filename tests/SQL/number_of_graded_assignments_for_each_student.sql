-- Write query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS num_graded_assignments
FROM Assignments
WHERE grade IS NOT NULL
GROUP BY student_id;
