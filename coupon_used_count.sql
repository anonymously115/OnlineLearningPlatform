SELECT
    a.*,
    IFNULL(b.used_count, 0) AS used_count
FROM
    teacher_coupon AS a
    LEFT OUTER JOIN (
        SELECT
            coupon_id,
            COUNT(*) AS used_count
        FROM
            student_coursepurchase
        GROUP BY
            coupon_id
    ) AS b ON a.id = b.coupon_id
WHERE
	applying_start_date <= date('now')
    AND date('now') <= applying_end_date;
    --AND available_count >= IFNULL(b.used_count, 0);