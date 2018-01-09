from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.validators import BLTIRoles
from blti.views import BLTIView, BLTILaunchView
from anonymous_feedback.models import Form, Comment


def _form_context(form, blti):
    context = form.json_data()

    try:
        BLTIRoles().validate(blti.data, 'admin')
        context['can_edit'] = True
        context['can_view_comments'] = True
    except BLTIException:
        pass

    return context


class LaunchView(BLTILaunchView):
    http_method_names = ['post']
    template_name = 'anonymous_feedback/form.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        course_id = self.blti.canvas_course_id

        form, created = Form.objects.get_or_create(course_id=course_id)
        if created:
            form.name = 'Leave anonymous feedback for %s' % (
                self.blti.course_short_name)
            form.save()

        return _form_context(form, self.blti)


class CommentView(BLTIView):
    http_method_names = ['get', 'options']
    template_name = 'anonymous_feedback/comments.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        form = Form.objects.get(course_id=self.blti.canvas_course_id)
        return _form_context(form, self.blti)


class EditView(CommentView):
    http_method_names = ['get', 'post', 'options']
    template_name = 'anonymous_feedback/edit.html'
    authorized_role = 'admin'

    def post(self, request, *args, **kwargs):
        try:
            form = Form.objects.get(course_id=self.blti.canvas_course_id)
            form.name = request.POST.get('name', None)
            form.description = request.POST.get('description', None)
            form.save()

            self.template_name = 'anonymous_feedback/form.html'
        except ValidationError as ex:
            pass

        return self.render_to_response(_form_context(form, self.blti))


class SubmitView(CommentView):
    http_method_names = ['post', 'options']
    template_name = 'anonymous_feedback/submit.html'
    authorized_role = 'member'

    def post(self, request, *args, **kwargs):
        course_id = self.blti.canvas_course_id
        content = request.POST.get('comments', '')

        try:
            form = Form.objects.get(course_id=course_id)
            form.add_comment(content=content)
        except ValidationError as ex:
            self.template_name = 'anonymous_feedback/form.html'

        return self.render_to_response(_form_context(form, self.blti))
