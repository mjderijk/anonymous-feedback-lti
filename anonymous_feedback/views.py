from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.views import BLTIView, BLTILaunchView
from anonymous_feedback.models import Form
from anonymous_feedback.dao.canvas import get_recipients_for_course


class LaunchView(BLTILaunchView):
    template_name = 'anonymous_feedback/form.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        user_id = blti_data.get('custom_canvas_user_id')
        #login_id = blti_data.get('custom_canvas_user_login_id', '')
        course_id = blti_data.get('custom_canvas_course_id')
        course_name = blti_data.get('context_label')

        instructors = get_recipients_for_course(course_id, user_id)
        blti_data['instructors'] = instructors
        self.set_session(request, **blti_data)

        return {'course_name': course_name, 'recipients': instructors}


class SubmitView(BLTIView):
    http_method_names = ['post', 'options']

    template_name = 'anonymous_feedback/submit.html'
    authorized_role = 'member'

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)

        sis_course_id = blti_data.get('lis_course_offering_sourcedid')
        course_name = blti_data.get('context_label')
        comments = request.POST.get('comments', '')

        recipients = []
        for user_id in request.POST.getlist('recipients', []):
            for instructor in blti_data['instructors']:
                if int(user_id) == instructor['user_id']:
                    recipients.append(instructor['email'])
                    break

        form, created = Form.objects.get_or_create(course_id=sis_course_id)

        context = {'course_name': course_name}
        try:
            form.send_feedback(recipients=recipients, comments=comments)
        except ValidationError as ex:
            self.template_name = 'anonymous_feedback/form.html'
            context['recipients'] = blti_data['instructors']

        return self.render_to_response(context)
