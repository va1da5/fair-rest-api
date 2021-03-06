# Generated by Django 3.1.8 on 2021-04-25 13:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Task Queue ID')),
                ('state', models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('ACTIVE', 'Active'), ('POSTPONED', 'Postponed'), ('COMPLETED', 'Completed')], default='SCHEDULED', help_text='Current task state', max_length=15, verbose_name='Task status')),
                ('postpone_counter', models.IntegerField(default=0, help_text='How many time the task was postponed', verbose_name='Postpone Count')),
                ('stars', models.IntegerField(blank=True, default=None, help_text='Self evaluation for the completion of the task in range of 1-5 starts', null=True, validators=[django.core.validators.MinValueValidator(1, message='Rating is to small'), django.core.validators.MaxValueValidator(5, message='Rating to too large')], verbose_name='Self rate')),
                ('scheduled_at', models.DateTimeField(auto_now_add=True, help_text='Time when the task was scheduled')),
                ('activated_at', models.DateTimeField(blank=True, default=None, help_text='Time when started working on the task', null=True)),
                ('postponed_at', models.DateTimeField(blank=True, default=None, help_text='Time when task was postponed', null=True)),
                ('completed_at', models.DateTimeField(blank=True, default=None, help_text='Time when task was completed', null=True)),
                ('task', models.ForeignKey(help_text='Task to be done', on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('user', models.ForeignKey(help_text='Assigned user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
