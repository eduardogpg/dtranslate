# Generated by Django 3.1.2 on 2020-10-07 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='status',
            field=models.IntegerField(choices=[(0, 'Processing'), (1, 'Upload'), (2, 'Transcribe'), (3, 'Translate'), (4, 'Subtitle')], default=0),
        ),
    ]
