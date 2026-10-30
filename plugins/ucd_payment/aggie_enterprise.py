"""Optional chartstring validation against the Aggie Enterprise GraphQL API.

Off unless every AGGIE_ENTERPRISE_* setting is configured.  The credentials (an OAuth client
credentials key, secret and scope) are issued per application by the Aggie Enterprise integration
team; https://github.com/ucdavis/AggieEnterpriseApi is their reference client.
"""
import time

import requests
from django.conf import settings

from .chartstring import GL, complete_gl

GL_QUERY = '''
query glValidateChartstring($segmentString: GlSegmentString!, $validateCVRs: Boolean) {
  glValidateChartstring(segmentString: $segmentString, validateCVRs: $validateCVRs) {
    validationResponse { valid errorMessages }
  }
}'''
PPM_QUERY = '''
query ppmSegmentStringValidate($segmentString: PpmSegmentString!) {
  ppmSegmentStringValidate(segmentString: $segmentString) {
    validationResponse { valid errorMessages }
  }
}'''

# The access token stays in process memory, never in the shared cache or database.
_token = {'value': None, 'expires': 0}


class AggieEnterpriseError(Exception):
    """Aggie Enterprise could not be reached, or did not answer the query."""


def is_configured():
    return all([settings.AGGIE_ENTERPRISE_GRAPHQL_URL, settings.AGGIE_ENTERPRISE_TOKEN_URL,
                settings.AGGIE_ENTERPRISE_CONSUMER_KEY, settings.AGGIE_ENTERPRISE_CONSUMER_SECRET,
                settings.AGGIE_ENTERPRISE_SCOPE])


def validate(chartstring):
    """Aggie Enterprise's error messages for a parsed chartstring; empty if it is valid."""
    if chartstring.kind == GL:
        name, document = 'glValidateChartstring', GL_QUERY
        variables = {'segmentString': complete_gl(chartstring.string), 'validateCVRs': True}
    else:
        name, document = 'ppmSegmentStringValidate', PPM_QUERY
        variables = {'segmentString': chartstring.string}
    data = query(document, variables)
    try:
        response = data[name]['validationResponse']
        if response['valid']:
            return []
        return response.get('errorMessages') or ['Aggie Enterprise reports that this chartstring is not valid.']
    except (KeyError, TypeError, AttributeError) as e:
        raise AggieEnterpriseError(f'Unexpected {name} response') from e


def query(document, variables):
    try:
        response = requests.post(settings.AGGIE_ENTERPRISE_GRAPHQL_URL, json={'query': document, 'variables': variables},
                                 headers={'Authorization': f'Bearer {get_token()}'}, timeout=settings.AGGIE_ENTERPRISE_TIMEOUT)
        if response.status_code == 401:
            forget_token()  # revoked or expired early; get a new one next time
        response.raise_for_status()
        body = response.json()
    except (requests.RequestException, ValueError) as e:
        raise AggieEnterpriseError(type(e).__name__) from e
    if not isinstance(body, dict) or body.get('errors') or not body.get('data'):
        raise AggieEnterpriseError(f'GraphQL errors: {str(body)[:500]}')
    return body['data']


def get_token():
    if _token['value'] and time.monotonic() < _token['expires']:
        return _token['value']
    try:
        response = requests.post(settings.AGGIE_ENTERPRISE_TOKEN_URL,
                                 data={'grant_type': 'client_credentials', 'scope': settings.AGGIE_ENTERPRISE_SCOPE},
                                 auth=(settings.AGGIE_ENTERPRISE_CONSUMER_KEY, settings.AGGIE_ENTERPRISE_CONSUMER_SECRET),
                                 timeout=settings.AGGIE_ENTERPRISE_TIMEOUT)
        response.raise_for_status()
        body = response.json()
        token, expires_in = body['access_token'], int(body.get('expires_in') or 0)
    except (requests.RequestException, ValueError, KeyError, TypeError, AttributeError) as e:
        raise AggieEnterpriseError(f'Token request failed: {type(e).__name__}') from e
    # Renew a minute early so a token never expires in the middle of a request.
    _token.update(value=token, expires=time.monotonic() + expires_in - 60)
    return token


def forget_token():
    _token.update(value=None, expires=0)
