# Generated by Django 3.1.2 on 2020-10-25 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20201025_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
    ]
