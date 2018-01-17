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
            'course_id': course_id,
            'can_edit': False,
        }

        try:
            self.authorize('admin')
            context['can_edit'] = True
            context['comments'] = form.comments()
        except BLTIException:
            pass

        return context
