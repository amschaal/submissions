"""
WSGI config for submissions project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'submissions.settings')

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()