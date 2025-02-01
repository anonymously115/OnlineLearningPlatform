INSERT INTO
    auth_user (
        id,
        username,
        password,
        first_name,
        last_name,
        email,
        is_superuser,
        is_staff,
        is_active,
        date_joined
    )
VALUES
    (
        0,
        '',
        '',
        '',
        '',
        '',
        FALSE,
        FALSE,
        FALSE,
        '0001-01-01 00:00:00'
    );

INSERT INTO
    online_learning_platform_account (
        user_ptr_id,
        teacher_flag,
        student_flag,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        FALSE,
        FALSE,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    online_learning_platform_teacher (account_ptr_id, profile)
VALUES
    (0, '');

INSERT INTO
    teacher_course (
        id,
        teacher_id,
        course_name,
        standard_price,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '',
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    teacher_section (
        id,
        course_id,
        section_no,
        section_name,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    teacher_content (
        id,
        section_id,
        content_no,
        content_name,
        content_flag,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '',
        FALSE,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    teacher_lecturevideo (content_ptr_id, lecture_time)
VALUES
    (0, 0);

INSERT INTO
    teacher_examination (content_ptr_id, answer_limit_time)
VALUES
    (0, 0);

INSERT INTO
    teacher_examquestion (
        id,
        exam_id,
        question_no,
        question_text,
        score,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '',
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    teacher_examquestionchoice (
        id,
        question_id,
        choice_no,
        choice_text,
        correct_answer_flag,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '',
        FALSE,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    teacher_coupon (
        id,
        course_id,
        applying_start_date,
        applying_end_date,
        available_count,
        coupon_issuing_date,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '0001-01-01',
        '0001-01-01',
        0,
        '0001-01-01',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    online_learning_platform_student (account_ptr_id, pay_info)
VALUES
    (0, '');

INSERT INTO
    student_coursepurchase (
        id,
        course_id,
        purchase_date,
        purchase_price,
        student_id,
        flag,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '0001-01-01',
        0,
        0,
        FALSE,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_courseattending (
        id,
        student_id,
        course_id,
        start_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_sectionattending (
        id,
        student_id,
        section_id,
        start_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_contentattending (
        id,
        student_id,
        content_id,
        start_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_examresult (contentattending_ptr_id, high_score)
VALUES
    (0, 0);

INSERT INTO
    student_examresultdetail (
        id,
        result_id,
        question_id,
        choice_id,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_examresulthistory (
        id,
        result_id,
        exam_execution_time,
        total_score,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '0001-01-01 00:00:00',
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_question (
        id,
        content_id,
        student_id,
        question_title,
        question_text,
        question_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '',
        '',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    student_comment (
        id,
        question_id,
        comment_text,
        comment_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_company (id, company_name, created_at, updated_at)
VALUES
    (
        0,
        '',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_corporateattendingstudent (student_ptr_id, company_id)
VALUES
    (0, 0);

INSERT INTO
    company_group (
        id,
        group_no,
        group_name,
        company_id,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '',
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_trainingcurriculum (
        id,
        training_curriculum_no,
        training_curriculum_name,
        company_id,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        '',
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_trainingcurriculumcourse (
        id,
        course_id,
        curriculum_id,
        attending_order,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_groupstudent (
        id,
        student_id,
        group_id,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_groupcurriculum (
        id,
        group_id,
        curriculum_id,
        date_startable_attending,
        attending_complete_deadline_date,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01',
        '0001-01-01',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_corporateattendingstudentcurriculum (
        id,
        student_id,
        curriculum_id,
        training_curriculum_attending_start_time,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );

INSERT INTO
    company_trainingcurriculumexam (
        id,
        exam_id,
        passing_base_point,
        curriculum_id,
        created_at,
        updated_at
    )
VALUES
    (
        0,
        0,
        0,
        0,
        '0001-01-01 00:00:00',
        '0001-01-01 00:00:00'
    );