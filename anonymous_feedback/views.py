from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.validators import BLTIRoles
from blti.views import BLTIView, BLTILaunchView
from anonymous_feedback.models import Form
from anonymous_feedback.dao.canvas import get_recipients_for_course


def _form_context(**kwargs):
    blti_data = kwargs.get('blti_params')
    sis_course_id = blti_data.get('lis_course_offering_sourcedid')

    form, created = Form.objects.get_or_create(course_id=sis_course_id)
    if created:
        course_name = blti_data.get('context_label')
        form.name = 'Send Anonymous Feedback for %s' % course_name
        form.save()

    context = form.json_data()
    context['recipients'] = blti_data['instructors']

    try:
        BLTIRoles().validate(blti_data, 'admin')
        context['can_edit'] = True
    except BLTIException:
        pass

    return context


class LaunchView(BLTILaunchView):
    template_name = 'anonymous_feedback/form.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        user_id = blti_data.get('custom_canvas_user_id')
        course_id = blti_data.get('custom_canvas_course_id')

        instructors = get_recipients_for_course(course_id, user_id)
        blti_data['instructors'] = instructors
        self.set_session(request, **blti_data)

        return _form_context(**kwargs)


class EditView(BLTIView):
    http_method_names = ['get', 'post', 'options']
    template_name = 'anonymous_feedback/edit.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid')

        try:
            form = Form.objects.get(course_id=sis_course_id)
        except Form.DoesNotExist:
            return self.render_to_response({}, status=401)

        return form.json_data()

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
            sis_course_id = blti_data.get('lis_course_offering_sourcedid')
            form = Form.objects.get(course_id=sis_course_id)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)
        except Form.DoesNotExist:
            return self.render_to_response({}, status=401)

        form.name = request.POST.get('name', None)
        form.description = request.POST.get('description', None)
        form.save()

        self.template_name = 'anonymous_feedback/form.html'
        context = _form_context(request=request, blti_params=blti_data)
        return self.render_to_response(context)


class SubmitView(BLTIView):
    http_method_names = ['post', 'options']
    template_name = 'anonymous_feedback/submit.html'
    authorized_role = 'member'

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
            sis_course_id = blti_data.get('lis_course_offering_sourcedid')
            form = Form.objects.get(course_id=sis_course_id)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)
        except Form.DoesNotExist:
            return self.render_to_response({}, status=401)

        comments = request.POST.get('comments', '')

        recipients = []
        for user_id in request.POST.getlist('recipients', []):
            for instructor in blti_data['instructors']:
                if int(user_id) == instructor['user_id']:
                    recipients.append(instructor['email'])
                    break

        try:
            form.send_feedback(recipients=recipients, comments=comments)
            context = form.json_data()
        except ValidationError as ex:
            self.template_name = 'anonymous_feedback/form.html'
            context = _form_context(request=request, blti_params=blti_data)

        return self.render_to_response(context)
