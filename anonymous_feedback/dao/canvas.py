from uw_canvas.users import Users


def get_instructors_for_course(course_id, user_id):
    return Users(as_user=user_id).get_users_for_course(course_id, params={
        'enrollment_type': ['teacher']})
