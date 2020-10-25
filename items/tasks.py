import os
from celery.decorators import task

@task(name='upload_video_file')
def upload_video_file(local_path, item_id):
    item = Item.objects.filter(id=item_id).first()
    
    if item:
        project = item.project
        project.upload_file()

        mediafile_key = f'{project.key}{item.name}'
        if put_object(bucket, mediafile_key, local_path):
            item.bucket = project.bucket
            item.key = mediafile_key
            item.save()

    os.remove(local_path)
 