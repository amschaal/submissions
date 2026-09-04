# Payment requirement per submission type, snapshotted onto each submission.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0018_submissiontype_internal'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='payment_required',
            field=models.BooleanField(default=True, help_text='Require payment information on submissions of this type.  The requirement is snapshotted onto each submission when it is created.'),
        ),
        migrations.AddField(
            model_name='submission',
            name='payment_required',
            field=models.BooleanField(default=True, help_text="Snapshot of the type's payment requirement when the submission was created.  Governs whether payment is shown and validated for the life of the submission."),
        ),
    ]
