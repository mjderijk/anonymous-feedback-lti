from uw_canvas.users import Users


def get_recipients_for_course(course_id):
    users = Users().get_users_for_course(course_id, params={
        'enrollment_type': ['teacher', 'ta'],
        'include': ['email']})

    recipients = []
    for user in users:
        if user.email is not None and len(user.email):
            recipients.append({'user_id': user.user_id,
                               'name': user.name,
                               'email': user.email})

    return recipients
