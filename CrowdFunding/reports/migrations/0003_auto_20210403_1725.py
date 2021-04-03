# Generated by Django 3.1.7 on 2021-04-03 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20210403_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('project_id', models.IntegerField(blank=True, null=True)),
                ('report_project', models.TextField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='report_comment',
            old_name='project_id',
            new_name='Comment_id',
        ),
    ]
