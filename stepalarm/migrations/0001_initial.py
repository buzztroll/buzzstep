# Generated by Django 5.1 on 2024-08-08 15:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('zero_offset', models.FloatField(default=0.0)),
                ('step_weight', models.FloatField()),
                ('threshold', models.FloatField(default=0.5)),
            ],
        ),
    ]
