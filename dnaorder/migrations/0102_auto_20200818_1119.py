# Generated by Django 2.2.6 on 2020-08-18 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnaorder', '0101_auto_20200814_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectid',
            options={'ordering': ('lab', 'prefix')},
        ),
        migrations.AlterField(
            model_name='submissiontype',
            name='prefix',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
