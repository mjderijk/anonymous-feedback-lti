from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
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

    course_id = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    sender_type = models.CharField(max_length=20,
                                   choices=SENDER_CHOICES,
                                   default=ANONYMOUS_SENDER)
    created_date = models.DateTimeField(auto_now_add=True)

    def json_data(self):
        return {
            'name': self.name if (self.name is not None) else '',
            'description': self.description if (
                self.description is not None) else '',
        }

    def send_feedback(self, sender=None, recipients=[], comments=''):
        sender = self.validate_sender(sender)
        comments = self.validate_comments(comments)
        recipients = self.validate_recipients(recipients)
        subject = 'Anonymous feedback'

        message = EmailMultiAlternatives(subject, comments, sender, recipients)

        try:
            message.send()
            log_message = 'Email sent'
        except Exception as ex:
            log_message = 'Email failed: %s' % ex

        for recipient in recipients:
            logger.info('%s, To: %s, Course: %s' % (
                log_message, recipient, self.course_id))

    def validate_sender(self, sender):
        if self.sender_type == self.ANONYMOUS_SENDER:
            return getattr(settings, 'EMAIL_NOREPLY_ADDRESS')

    def validate_comments(self, comments):
        comments = comments.strip()
        if not len(comments):
            raise ValidationError('todo', code='missing')
        return comments

    def validate_recipients(self, recipients):
        if not len(recipients):
            raise ValidationError('todo', code='missing')
        return recipients
