import os
from datetime import datetime

from AWS import transcribe
from AWS import subtitles
from AWS import upload_file
from AWS import set_public_object

from celery.decorators import task

from items.models import Item

@task(name='start_transcribe_and_translate')
def delete_file(local_path):
    os.remove(local_path)

@task(name='start_transcribe_and_translate')
def start_transcribe_and_translate(local_path, item_id, target):
    print('Subiendo vídeo')
    upload_video_file(local_path, item_id)
    
    print('Generando transcripción')
    transcribe_item = start_transcribe(item_id)
    
    print('Generando subtitulos')
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
    now = datetime.now().strftime('%Y_%m_%d')

    item = Item.objects.filter(id=transcribe_id).first()
    project = item.project

    source = item.lenguage.split('-')[0]
    target = target.split('-')[0]

    subtitle_name = f'{source}_{project.name}_{now}.srt'
    subtitle_translate_name = f'{target}_{project.name}_{now}.srt'

    subtitle_key, subtitle_translate_key = subtitles(
        project.bucket, item.key,
        subtitle_name, subtitle_translate_name,
        project.key, source, target
    )

    Item.objects.create(
        name=subtitle_name,
        bucket=project.bucket,
        key=subtitle_key,
        content_type='text/srt',
        project=project,
        lenguage=item.lenguage
    )

    Item.objects.create(
        name=subtitle_translate_name,
        bucket=project.bucket,
        key=subtitle_translate_key,
        content_type='text/srt',
        project=project,
        lenguage=item.lenguage
    )