-- Write query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS graded_assignment_count
FROM assignments
WHERE grade IS NOT NULL  -- Only count assignments that have been graded
GROUP BY student_id
ORDER BY student_id;
