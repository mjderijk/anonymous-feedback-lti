Anonymous Feedback LTI App
===========================

A Django LTI application that allows course members to submit anonymous comments.

Installation
------------

**Project directory**

Install the app in your project.

    $ cd [project]
    $ pip install Anonymous-Feedback-LTI

Project settings.py
------------------

**INSTALLED_APPS**

    'anonymous_feedback',
    'blti',

**REST client app settings**

    RESTCLIENTS_CANVAS_DAO_CLASS = 'Live'
    RESTCLIENTS_CANVAS_HOST = 'example.instructure.com'
    RESTCLIENTS_CANVAS_OAUTH_BEARER = '...'

**BLTI settings**

[django-blti settings](https://github.com/uw-it-aca/django-blti#project-settingspy)

Project urls.py
---------------
    url(r'^anonymous_feedback/', include('anonymous_feedback.urls')),
