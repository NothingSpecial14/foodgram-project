# Generated by Django 5.0.7 on 2024-10-27 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 10, 27, 8, 5, 8, 949455, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]