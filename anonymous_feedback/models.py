from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger(__name__)


class Form(models.Model):
    ANONYMOUS_SENDER = 'anonymous'
    OPTIONAL_SENDER = 'optional'
    REQUIRED_SENDER = 'required'

    SENDER_CHOICES = (
        (ANONYMOUS_SENDER, 'Anonymous'),
        (OPTIONAL_SENDER, 'Optional'),
        (REQUIRED_SENDER, 'Required')
    )

    course_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    sender_type = models.CharField(max_length=20,
                                   choices=SENDER_CHOICES,
                                   default=ANONYMOUS_SENDER)
    created_date = models.DateTimeField(auto_now_add=True)

    def json_data(self):
        return {
            'course_id': self.course_id,
            'name': self.name if (self.name is not None) else '',
            'description': self.description if (
                self.description is not None) else '',
            'created_date': self.created_date.isoformat(),
            'comments': self.comment_set.all(),
        }

    def add_comment(self, comment_str):
        comment_str = self.validate_comment(comment_str)
        comment = self.comment_set.create(comment=comment_str)

        #TODO: notify instructors?

    def validate_comment(self, comment):
        comment = comment.strip()
        if not len(comment):
            raise ValidationError('Missing comment', code='missing')
        return comment


class Comment(models.Model):
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def json_data(self):
        return {
            'comment': self.comment,
            'created_date': self.created_date.isoformat(),
        }
