# Generated by Django 3.1.2 on 2020-10-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(default='CREATED', max_length=20),
        ),
    ]
