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
        form = Form.objects.get(course_id=self.blti.canvas_course_id)
        return self.json_response(form.json_data())

    def put(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get(course_id=self.blti.canvas_course_id)
        try:
            data = json.loads(request.body)
            form.name = data.get('name')
            form.description = data.get('description')
            form.save()
        except ValidationError as ex:
            return self.error_json(400, err)

        return self.json_response(form.json_data())


class CommentsAPI(RESTDispatch):
    authorized_role = 'member'

    def get(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get(course_id=self.blti.canvas_course_id)

        data = form.json_data()
        data['comments'] = [c.json_data() for c in form.comments()]
        return self.json_response(data)

    def post(self, request, *args, **kwargs):
        form = Form.objects.get(course_id=self.blti.canvas_course_id)

        try:
            data = json.loads(request.body)
            form.add_comment(content=data.get('content'))
        except ValidationError as err:
            return self.error_json(400, err)

        return self.json_response(form.json_data())

    def delete(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get(course_id=self.blti.canvas_course_id)

class CommentAPI(RESTDispatch):
    authorized_role = 'admin'

    def delete(self, request, *args, **kwargs):
        try:
            self.authorize('admin')
        except BLTIException as err:
            return self.error_response(401, err)

        form = Form.objects.get(course_id=self.blti.canvas_course_id)