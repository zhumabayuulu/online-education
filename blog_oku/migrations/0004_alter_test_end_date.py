# Generated by Django 4.0.4 on 2023-04-16 23:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog_oku', '0003_alter_test_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 26, 23, 1, 54, 755719, tzinfo=utc)),
        ),
    ]
