# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-02 19:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edx_proctoring', '0006_allowed_time_limit_mins'),
    ]

    operations = [
        migrations.AddField(
            model_name='proctoredexam',
            name='backend',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
