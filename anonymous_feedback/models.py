from django.db import models
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger(__name__)


class FormManager(models.Manager):
    def get_by_course_id(self, course_id):
        return Form.objects.get(course_id=course_id)


class Form(models.Model):
    ANONYMOUS_COMMENTER = 'anonymous'
    OPTIONAL_COMMENTER = 'optional'
    REQUIRED_COMMENTER = 'required'

    COMMENTER_CHOICES = (
        (ANONYMOUS_COMMENTER, 'Anonymous'),
        (OPTIONAL_COMMENTER, 'Optional'),
        (REQUIRED_COMMENTER, 'Required')
    )

    course_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    commenter_type = models.CharField(max_length=20,
                                      choices=COMMENTER_CHOICES,
                                      default=ANONYMOUS_COMMENTER)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = FormManager()

    class Meta:
        app_label = 'anonymous_feedback'

    def json_data(self, include_comments=False):
        data = {
            'course_id': self.course_id,
            'name': self.name if (self.name is not None) else '',
            'description': self.description if (
                self.description is not None) else '',
            'type': self.commenter_type,
            'comment_count': self.comment_set.count(),
        }

        if include_comments:
            data['comments'] = [c.json_data() for c in self.comments()]

        return data

    def comments(self):
        return self.comment_set.all().order_by('-created_date')

    def add_comment(self, content=''):
        content = self.validate_comment(content)
        return self.comment_set.create(content=content)

    def delete_comment(self, comment_id):
        for comment in self.comments():
            if comment.id == comment_id:
                comment.delete()
                break

    def delete_all_comments(self):
        self.comment_set.all().delete()

    def validate_comment(self, content):
        if content is None:
            raise ValidationError('Missing comment', code='missing')

        content = content.strip()
        if not len(content):
            raise ValidationError('Missing comment', code='missing')
        return content


class Comment(models.Model):
    user_id = models.IntegerField(null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        app_label = 'anonymous_feedback'

    def json_data(self):
        return {
            'comment_id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'created_date': self.created_date.isoformat(),
        }
