"""File fields in submission schemas: {"type": "string", "format": "file", "template": <LabFile id>,
"accept": ".xlsx,.csv", "max_size_mb": 10}. The submission data holds the id of a SubmissionFile, which is
uploaded first (unattached) and attached to the submission when the submission is saved."""
import os
from datetime import timedelta

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone

FILE_FORMAT = 'file'
PENDING_HOURS = 24  # unattached uploads expire after this and are removed by `manage.py cleanup_uploads`


def is_file_field(definition):
    return definition.get('format') == FILE_FORMAT


def file_variables(schema):
    return [v for v, d in (schema or {}).get('properties', {}).items() if is_file_field(d)]


def upload_error(definition, name, size):
    """Why a file can't be used for the field, or None."""
    extensions = [e.strip().lower() for e in (definition.get('accept') or '').split(',') if e.strip().startswith('.')]
    if extensions and os.path.splitext(name)[1].lower() not in extensions:
        return 'Only {} files are accepted.'.format(', '.join(extensions))
    max_size_mb = definition.get('max_size_mb')
    if max_size_mb and size > float(max_size_mb) * 1024 * 1024:
        return 'Files may not be larger than {} MB.'.format(max_size_mb)
    return None


def pending_cutoff():
    return timezone.now() - timedelta(hours=PENDING_HOURS)


def validate_file_fields(schema, data, submission=None):
    """Each file field must hold the id of an upload for that field which is either unattached and
    unexpired, or already attached to this submission. Returns (errors, ids of uploads to attach)."""
    from dnaorder.models import SubmissionFile
    errors, pending = {}, []
    for variable in file_variables(schema):
        file_id = data.get(variable)
        if file_id in (None, ''):
            continue
        upload = SubmissionFile.objects.filter(id=str(file_id), variable=variable).first()
        if upload and submission and upload.submission_id == submission.id:
            continue
        if not upload or upload.submission_id is not None or upload.uploaded_at < pending_cutoff():
            errors[variable] = ['The uploaded file was not found or has expired. Please upload it again.']
            continue
        error = upload_error(schema['properties'][variable], upload.get_filename(), upload.file.size)
        if error:
            errors[variable] = [error]
            continue
        pending.append(upload.id)
    return errors, pending


def attach_uploads(submission, file_ids):
    """Attach validated uploads; fails if another submission attached one of them in the meantime."""
    from dnaorder.models import SubmissionFile
    attached = SubmissionFile.objects.filter(id__in=file_ids, submission__isnull=True).update(submission=submission)
    if attached != len(set(file_ids)):
        from rest_framework.exceptions import ValidationError
        raise ValidationError({'submission_data': ['An uploaded file is already used by another submission. Please upload it again.']})


def template_errors(schema, lab):
    """File field templates must be public files of the submission type's lab, so submitters can download them."""
    from dnaorder.models import LabFile
    errors = []
    for variable in file_variables(schema):
        template = schema['properties'][variable].get('template')
        if not template:
            continue
        try:
            lab_file = LabFile.objects.filter(pk=template, lab=lab).first()
        except (ValueError, DjangoValidationError):  # not a UUID
            lab_file = None
        if not lab_file:
            errors.append('"{}": the template must be one of this lab\'s files.'.format(variable))
        elif lab_file.internal:
            errors.append('"{}": the template "{}" is internal, so submitters could not download it.'.format(variable, lab_file.name))
    return errors
