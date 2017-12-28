from django.db import models


class FormManager(models.Manager):
    pass


class Form(models.Model):
    ANONYMOUS_AUTH = 'anonymous'
    OPTIONAL_AUTH = 'optional'
    REQUIRED_AUTH = 'required'

    AUTH_CHOICES = (
        (ANONYMOUS_AUTH, 'Anonymous'),
        (OPTIONAL_AUTH, 'Optional'),
        (REQUIRED_AUTH, 'Required')
    )

    subject = models.CharField(max_length=256)
    comments = models.TextField()
    auth_type = models.CharField(max_length=20, choices=AUTH_CHOICES)
    created_by = models.CharField(max_length=32)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.NullBooleanField()
    deleted_date = models.DateTimeField(null=True)

    objects = FormManager()
