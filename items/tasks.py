import os

from AWS import transcribe
from AWS import upload_file
from AWS import set_public_object

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
        if upload_file(project.bucket, mediafile_key, local_path, item.content_type):
            item.key = mediafile_key
            item.bucket = project.bucket
            item.save()
            
            project.file_uploaded()
            os.remove(local_path)

            set_public_object(item.bucket, item.key)

@task(name='start_transcribe')
def start_transcribe(video_item_id):
    item = Item.objects.filter(id=video_item_id).first()
    
    if item:
        project = item.project
        project.transcribe()

        mediafile_key = transcribe(project.bucket, project.key, item.uri, project.name,
                                format=item.format, lenguage=item.lenguage)

        item_transcribe = Item.objects.creat(
            name=mediafile_key,
            bucket=project.bucket,
            key=f'{project.key}{mediafile_key}' ,
            content_type='application/json',
            project=project,
            lenguage=item.lenguage
        )

@task(name='start_substitles')
def start_substitles(target):
    pass