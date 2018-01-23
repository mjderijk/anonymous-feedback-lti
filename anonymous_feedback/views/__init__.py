from django.http import HttpResponse
from django.urls import reverse
from blti import BLTIException
from blti.views import BLTILaunchView, BLTIView
from anonymous_feedback.models import Form
from logging import getLogger
import csv
import re


logger = getLogger(__name__)


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
                'comments_file': reverse(
                    'comments-file', kwargs={'course_id': course_id}),
            })
        except BLTIException:
            pass

        return context


class CommentsFileView(BLTIView):
    authorized_role = 'admin'

    def post(self, request, *args, **kwargs):
        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (
            re.sub(r'[,/]', '-', form.name))

        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(response, dialect='unix_newline')
        writer.writerow(['Date', 'Comment'])

        for comment in form.comments():
            writer.writerow([comment.created_date.isoformat(),
                             comment.content])

        return response
