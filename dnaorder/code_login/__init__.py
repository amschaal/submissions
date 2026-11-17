"""Emailed one-time-code login for users without lab or institution permissions.

Built on django-allauth's ``account`` and ``headless`` apps.  Only two endpoints
are mounted (request a code, confirm a code); see ``urls.py``.  Lab staff and
institution admins keep signing in through Keycloak.
"""
