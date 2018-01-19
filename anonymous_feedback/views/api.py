from django.http import HttpResponse
from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.views import RESTDispatch
from anonymous_feedback.models import Form
from logging import getLogger
import json
import csv
import re


logger = getLogger(__name__)


class FormAPI(RESTDispatch):
    authorized_role = 'member'

    def get(self, request, *args, **kwargs):
        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)
        return self.json_response(form.json_data())

    def put(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)
        try:
            data = json.loads(request.body)
            form.name = data.get('name')
            form.description = data.get('description')
            form.save()
        except (ValueError, ValidationError) as err:
            return self.error_response(400, err)

        return self.json_response(form.json_data())


class CommentsAPI(RESTDispatch):
    authorized_role = 'member'

    def get(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)

        content_type = kwargs.get('content_type', '').lower()
        if 'csv' in content_type:
            return self.csv_response(form.comments(), filename=form.name)

        data = form.json_data()
        data['comments'] = [c.json_data() for c in form.comments()]
        return self.json_response(data)

    def post(self, request, *args, **kwargs):
        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)

        try:
            data = json.loads(request.body)
            form.add_comment(content=data.get('content'))
        except (ValueError, ValidationError) as err:
            return self.error_response(400, err)

        return self.json_response(form.json_data())

    def delete(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)
        form.delete_all_comments()

        return self.json_response(form.json_data())

    def csv_response(self, comments, status=200, filename='file'):
        response = HttpResponse(status=status, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (
            re.sub(r'[,/]', '-', filename))

        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(response, dialect='unix_newline')
        writer.writerow(['Date', 'Comment'])

        for comment in comments:
            writer.writerow([comment.created_date.isoformat(),
                             comment.content])

        return response


class CommentAPI(RESTDispatch):
    authorized_role = 'admin'

    def delete(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)
