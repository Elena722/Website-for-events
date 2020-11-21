# Generated by Django 3.1.3 on 2020-11-20 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('event_type', models.CharField(choices=[('offline event', 'offline event'), ('online event', 'online event')], default='offline', max_length=20)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('description', models.TextField(null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('members_number', models.PositiveIntegerField(default=0)),
                ('host', models.CharField(max_length=30, null=True)),
                ('cover', models.ImageField(blank=True, default='./images/covers/fon.jpeg', null=True, upload_to='./images/covers/')),
                ('created', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.category')),
                ('join', models.ManyToManyField(blank=True, related_name='join', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_date', 'start_time', 'end_date', 'end_time'],
            },
        ),
        migrations.CreateModel(
            name='JoinModelButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Join', 'Join'), ('UnJoin', 'UnJoin')], default='Join', max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
