from django.db import models


class Form(models.Model):
    ANONYMOUS_SENDER = 'anonymous'
    OPTIONAL_SENDER = 'optional'
    REQUIRED_SENDER = 'required'

    SENDER_CHOICES = (
        (ANONYMOUS_SENDER, 'Anonymous'),
        (OPTIONAL_SENDER, 'Optional'),
        (REQUIRED_SENDER, 'Required')
    )

    course_id = models.CharField(max_length=80)
    subject = models.CharField(max_length=256)
    comments = models.TextField()
    sender_type = models.CharField(max_length=20,
                                   choices=SENDER_CHOICES,
                                   default=OPTIONAL_SENDER)
    created_date = models.DateTimeField(auto_now_add=True)
