# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept_name', models.CharField(max_length=50)),
                ('dept_id', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registered_Employee_Detail',
            fields=[
                ('emp_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('emp_first_name', models.CharField(max_length=50, null=True)),
                ('emp_last_name', models.CharField(max_length=50)),
                ('emp_full_name', models.CharField(max_length=200)),
                ('emp_email', models.EmailField(unique=True, max_length=75)),
                ('emp_password', models.CharField(max_length=50)),
                ('emp_address', models.TextField()),
                ('emp_gender', models.CharField(max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('emp_marital_status', models.CharField(max_length=15, choices=[(b'Married', b'Married'), (b'Unmarried', b'Unmarried')])),
                ('emp_contact_number', models.IntegerField(max_length=13)),
                ('emp_role', models.CharField(max_length=20, null=True, choices=[(b'Admin', b'Admin'), (b'User', b'User')])),
                ('emp_profile_pic', models.CharField(default=b'avatar.jpg', max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salary', models.FloatField()),
                ('bonus', models.IntegerField(null=True, blank=True)),
                ('emp_id', models.ForeignKey(to='employeeapp.Registered_Employee_Detail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField(auto_now=True)),
                ('logout_time', models.DateTimeField(blank=True)),
                ('emp_id', models.ForeignKey(to='employeeapp.Registered_Employee_Detail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='department',
            name='emp_id',
            field=models.ForeignKey(to='employeeapp.Registered_Employee_Detail'),
            preserve_default=True,
        ),
    ]
