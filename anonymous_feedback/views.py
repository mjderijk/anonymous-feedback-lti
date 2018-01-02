from blti import BLTIException
from blti.views import BLTIView, BLTILaunchView
from anonymous_feedback.models import Form
from anonymous_feedback.dao.canvas import get_instructors_for_course


class LaunchView(BLTILaunchView):
    template_name = 'anonymous_feedback/form.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        user_id = blti_data.get('custom_canvas_user_id')
        login_id = blti_data.get('custom_canvas_user_login_id', '')
        course_id = blti_data.get('custom_canvas_course_id')

        instructors = get_instructors_for_course(course_id, user_id)

        return {}


class SubmitFeedbackView(BLTIView):
    template_name = 'anonymous_feedback/submit.html'
    authorized_role = 'member'

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)

        course_id = blti_data.get('custom_canvas_course_id')

        form, created = Form.objects.get_or_create(course_id=course_id)

        context = self.get_context_data(
            request=request, blti_params=blti_data, **kwargs)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
