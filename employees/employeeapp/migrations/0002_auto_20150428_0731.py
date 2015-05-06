# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employeeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered_employee_detail',
            name='emp_profile_pic',
            field=models.CharField(default=b'avatar.png', max_length=200),
        ),
    ]
