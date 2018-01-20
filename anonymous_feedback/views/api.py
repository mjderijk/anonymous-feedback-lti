from django.core.exceptions import ValidationError
from blti import BLTIException
from blti.views import RESTDispatch
from anonymous_feedback.models import Form
from logging import getLogger
import json


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

        return self.json_response(form.json_data(include_comments=True))

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

        return self.json_response(form.json_data(include_comments=True))


class CommentAPI(RESTDispatch):
    authorized_role = 'admin'

    def delete(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        comment_id = kwargs.get('comment_id')

        form = Form.objects.get_by_course_id(self.blti.canvas_course_id)
        form.delete_comment(comment_id)

        return self.json_response(form.json_data(include_comments=True))
