# Test package for the core dnaorder API.
#
# Run inside the api container:
#     docker compose exec api python manage.py test dnaorder
#
# Focus areas (see individual modules):
#   test_authentication.py   - auth is enforced on protected endpoints
#   test_open_endpoints.py   - intentionally-public endpoints stay public
#   test_permissions_tenancy.py - multi-tenant isolation / IDOR / permission tiers
#   test_security.py         - active vulnerability probes
#   test_throttling.py       - DRF throttling is enforced (429)
#   test_endpoint_behavior.py - endpoints behave correctly for happy paths
#   test_payment_required.py - SubmissionType.payment_required and its per-submission snapshot
