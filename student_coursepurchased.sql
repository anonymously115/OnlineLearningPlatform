SELECT
    *
FROM
    teacher_course AS a
    LEFT OUTER JOIN student_coursepurchase AS b ON a.id = b.course_id;