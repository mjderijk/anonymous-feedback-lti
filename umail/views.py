from blti.views import BLTILaunchView


class LaunchView(BLTILaunchView):
    template_name = 'umail/home.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        login_id = blti_data.get('custom_canvas_user_login_id', '')
        course_id = blti_data.get('custom_canvas_course_id')

        return {}
