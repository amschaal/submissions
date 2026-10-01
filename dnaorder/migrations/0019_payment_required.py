# Per-type payment requirement.  Submissions that already carry payment data
# keep it regardless (see Submission.payment_required).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0018_submissiontype_internal'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='payment_required',
            field=models.BooleanField(default=True, help_text='Require payment information on submissions of this type.  Submissions that already have payment information keep it regardless.'),
        ),
    ]
