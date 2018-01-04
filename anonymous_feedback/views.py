from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.validators import BLTIRoles
from blti.views import BLTIView, BLTILaunchView
from anonymous_feedback.models import Form, Comment


def _form_context(blti_data):
    course_id = blti_data.get('custom_canvas_course_id')

    form, created = Form.objects.get_or_create(course_id=course_id)
    if created:
	course_name = blti_data.get('context_label')
	form.name = 'Send Anonymous Feedback for %s' % course_name
	form.save()

    context = form.json_data()

    try:
        BLTIRoles().validate(blti_data, 'admin')
        context['can_edit'] = True
        context['can_view_comments'] = True
    except BLTIException:
        pass

    return context


class LaunchView(BLTILaunchView):
    template_name = 'anonymous_feedback/form.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        return _form_context(kwargs.get('blti_params'))


class EditView(BLTIView):
    http_method_names = ['get', 'post', 'options']
    template_name = 'anonymous_feedback/edit.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        return _form_context(kwargs.get('blti_params'))

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
            course_id = blti_data.get('custom_canvas_course_id')
            form = Form.objects.get(course_id=course_id)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)
        except Form.DoesNotExist:
            return self.render_to_response({}, status=401)

        form.name = request.POST.get('name', None)
        form.description = request.POST.get('description', None)
        form.save()

        self.template_name = 'anonymous_feedback/form.html'
        return self.render_to_response(_form_context(blti_data))


class CommentView(BLTIView):
    template_name = 'anonymous_feedback/comments.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        return _form_context(kwargs.get('blti_params'))


class SubmitView(BLTIView):
    http_method_names = ['post', 'options']
    template_name = 'anonymous_feedback/submit.html'
    authorized_role = 'member'

    def post(self, request, *args, **kwargs):
        try:
            blti_data = self.validate(request)
            course_id = blti_data.get('custom_canvas_course_id')
            form = Form.objects.get(course_id=course_id)
        except BLTIException as err:
            self.template_name = 'blti/401.html'
            return self.render_to_response({}, status=401)
        except Form.DoesNotExist:
            return self.render_to_response({}, status=401)

        comment_str = request.POST.get('comments', '')

        try:
            form.add_comment(comment_str)
        except ValidationError as ex:
            self.template_name = 'anonymous_feedback/form.html'

        return self.render_to_response(_form_context(blti_data))
