# Generated by Django 3.1.2 on 2020-10-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='title',
        ),
        migrations.AddField(
            model_name='item',
            name='bucket',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
