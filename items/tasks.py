import os

from AWS import transcribe
from AWS import subtitles
from AWS import upload_file
from AWS import set_public_object

from celery.decorators import task

from items.models import Item

@task(name='start_transcribe_and_translate')
def start_transcribe_and_translate(local_path, item_id, target):
    print('Subiendo vídeo')
    upload_video_file(local_path, item_id)
    
    print('Comenzando transcribe')
    transcribe_item = start_transcribe(item_id)
    
    print('Comenzando substiles')
    start_substitles(transcribe_item.id, target)

@task(name='upload_video_file')
def upload_video_file(local_path, item_id):
    item = Item.objects.filter(id=item_id).first()
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
def start_transcribe(video_id):
    item = Item.objects.filter(id=video_id).first()
    project = item.project

    project.transcribe()

    mediafile_key = transcribe(project.bucket, project.key, item.uri, project.name,
                                format=item.format, lenguage=item.lenguage)

    return Item.objects.create(
        name=mediafile_key,
        bucket=project.bucket,
        key=f'{project.key}{mediafile_key}' ,
        content_type='application/json',
        project=project,
        lenguage=item.lenguage
    )

@task(name='start_substitles')
def start_substitles(transcribe_id, target):
    item = Item.objects.filter(id=transcribe_id).first()
    project = item.project

    source = item.lenguage.split('-')[0]
    target = target.split('-')[0]

    s_key, t_key = subtitles(item.bucket, item.key, project.name, project.key, source, target)