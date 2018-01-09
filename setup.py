import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/anonymous-feedback-lti>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'anonymous_feedback/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Anonymous-Feedback-LTI',
    version=VERSION,
    packages=['anonymous_feedback'],
    include_package_data=True,
    install_requires = [
        'Django>=1.10,<1.11',
        'django-blti>=1.2',
        'Django-Safe-EmailBackend>=0.1,<1.0',
        'UW-RestClients-Canvas>=0.6.6,<1.0',
    ],
    license='Apache License, Version 2.0',
    description='An LTI app that allows people to send you anonymous email directly to your email inbox.',
    long_description=README,
    url='https://github.com/uw-it-aca/anonymous-feedback-lti',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
