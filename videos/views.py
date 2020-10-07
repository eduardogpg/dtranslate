import os
import threading

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from .models import Video
from .constants import LENGUAGES

from AWS import upload_file
from AWS import transcribe
from AWS import translate_from_mediafile
from AWS import create_and_upload_subtitle_file

def upload_and_translate_video(local_path, lenguage, video_id):
    video = Video.objects.get(pk=video_id)
    video.upload()

    print('Comienza la subida del archivo!')
    response = upload_file(video.bucket, video.title,
                            local_path, video.content_type)

    if response:
        print('Comienza el transcribe!')
        video.transcribe()
        translate_key = transcribe(video.bucket, video.url,
                                    name=video.name, lenguage=lenguage, format=video.format)
        
        print('Comienza el translate!')
        video.traslate()
        translate_from_mediafile(video.bucket, translate_key)

        print('Comienza el subtitle!')
        video.subtitle()
        create_and_upload_subtitle_file(video.bucket, translate_key)

        video.completed()
        delete_uploaded_file(local_path)
        
def create(request):
    
    context = {
        'title': 'Nuevo vídeo',
        'lenguages': LENGUAGES,
    }

    if request.method == 'POST':        
        if request.FILES.get('video') and request.POST.get('lenguage'):
            lenguage = request.POST['lenguage']
            video_file = request.FILES['video']
            
            local_path = handle_uploaded_file(video_file)
            if local_path:
                
                video = Video.objects.create(title=video_file._name,
                                            bucket=settings.BUCKET,
                                            content_type=video_file.content_type)
                
                args = (local_path, lenguage, video.id)
                thread = threading.Thread(target=upload_and_translate_video, args=args)
                thread.start()
                
                messages.success(request, 'Vídeo procesado de forma exitosa!')
                
                return redirect('videos:detail', pk=video.pk)

            else:
                messages.error(request, 'No fue posible crear el archivo.')
        else:
            messages.error(request, 'Es necesario ingresar los datos requeridos.')

    return render(request, 'videos/create.html', context)

def detail(request, pk):
    video = Video.objects.get(pk=pk)
    
    context = {
        'title': video.title,
        'video': video,
    }

    return render(request, 'videos/detail.html', context)

def handle_uploaded_file(file):
    try:
        local_path = f'{settings.TMP_DIR}/{file}'
        print(local_path)

        with open(local_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return local_path

    except Exception as err:
        print(err)
        return None

def delete_uploaded_file(local_path):
    if os.path.exists(local_path):
        os.remove(local_path)

