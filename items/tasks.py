import os

from AWS import transcribe
from AWS import put_object

from celery.decorators import task

from items.models import Item

@task(name='start_transcribe_and_translate')
def start_transcribe_and_translate(local_path, item_id, target):
    upload_video_file(local_path, item_id)
    start_transcribe(item_id)

@task(name='upload_video_file')
def upload_video_file(local_path, item_id):
    item = Item.objects.filter(id=item_id).first()
    
    if item:
        project = item.project
        project.uploading_file()

        mediafile_key = f'{project.key}{item.name}'
        if put_object(project.bucket, mediafile_key, local_path):
            item.key = mediafile_key
            item.bucket = project.bucket
            item.location = project.location
            item.save()
            
            project.file_uploaded()
            os.remove(local_path)

@task(name='start_transcribe')
def start_transcribe(video_item_id):
    item = Item.objects.filter(id=video_item_id).first()
    
    if item:
        project = item.project
        project.transcribe()

        transcribe_uri = transcribe(project.bucket, item.uri, project.name, format=item.format, lenguage=item.lenguage)
    
        item_transcribe = Item.objects.creat(
            name='transcribe!!!',
            bucket=item.bucket,
            key=transcribe_uri,
            content_type='application/json',
            project=project,
            lenguage=item.lenguage
        )

@task(name='start_substitles')
def start_substitles(target):
    pass