from django.urls import reverse
from blti import BLTIException
from blti.views import BLTILaunchView
from anonymous_feedback.models import Form


class LaunchView(BLTILaunchView):
    template_name = 'anonymous_feedback/main.html'
    authorized_role = 'member'

    def get_context_data(self, **kwargs):
        course_id = self.blti.canvas_course_id

        form, created = Form.objects.get_or_create(course_id=course_id)
        if created:
            form.name = 'Leave anonymous feedback for %s' % (
                self.blti.course_short_name)
            form.save()

        context = {
            'session_id': self.request.session.session_key,
            'can_edit': False,
            'comments_api': reverse(
                'comments-api', kwargs={'course_id': course_id}),
        }

        try:
            self.authorize('admin')
            context.update({
                'can_edit': True,
                'comment_count': len(form.comments()),
                'form_api': reverse(
                    'form-api', kwargs={'course_id': course_id}),
                'comments_download_api': reverse(
                    'comments-api',
                    kwargs={'course_id': course_id, 'content_type': '.csv'}),
            })
        except BLTIException:
            pass

        return context
