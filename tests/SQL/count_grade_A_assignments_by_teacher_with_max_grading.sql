-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradeCounts AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments
    FROM assignments
    WHERE teacher_id IS NOT NULL
    GROUP BY teacher_id
),
MaxTeacher AS (
    SELECT 
        teacher_id
    FROM TeacherGradeCounts
    ORDER BY total_assignments DESC, teacher_id ASC
    LIMIT 1
)
SELECT 
    COUNT(*) AS grade_a_count
FROM assignments
WHERE 
    grade = 'A' 
    AND teacher_id = (SELECT teacher_id FROM MaxTeacher);


