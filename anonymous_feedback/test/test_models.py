from django.test import TestCase
from django.core.exceptions import ValidationError
from anonymous_feedback.models import Form, Comment


class FormTest(TestCase):
    def setUp(self):
        self.form = Form(course_id=123)
        self.form.save()

        self.form.comment_set.create(content='1')
        self.form.comment_set.create(content='2')

    def test_add_comment(self):
        self.assertEquals(self.form.comment_set.count(), 2)

        comment = self.form.add_comment('Test')
        self.assertEquals(self.form.comment_set.count(), 3)
        self.assertEquals(comment.content, 'Test')

    def test_validate_comment(self):
        self.assertEquals(self.form.validate_comment('Test'), 'Test')
        self.assertEquals(self.form.validate_comment(' Test   '), 'Test')
        self.assertRaises(ValidationError, self.form.validate_comment, None)
        self.assertRaises(ValidationError, self.form.validate_comment, '')
        self.assertRaises(ValidationError, self.form.validate_comment, '    ')

    def test_delete_comment(self):
        self.assertEquals(self.form.comment_set.count(), 2)

        comment = self.form.add_comment('Test')

        self.form.delete_comment(comment.id)
        self.assertEquals(self.form.comment_set.count(), 2)

    def test_delete_all_comments(self):
        self.assertEquals(self.form.comment_set.count(), 2)

        self.form.delete_all_comments()
        self.assertEquals(self.form.comment_set.count(), 0)
