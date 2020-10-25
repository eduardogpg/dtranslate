import multiprocessing

from django.conf import settings
from django.shortcuts import render

from .models import Item
from projects.models import Project

from .forms import UploadFileForm

def upload_video_file(local_path, item):
    print('\n\n\n\nComenzando subida')
    print('\n\n\n\n\nComenzando subida Finalizadaa!!!!')

def create(request):
    form = UploadFileForm(request.POST or None)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.cleaned_data['file']
            name = video._name.split('.')[0].lower().replace(' ', '_')

            project = Project.objects.create_by_aws(settings.BUCKET, name)
            
            local_path = f'tmp/{video._name}'
            if handle_uploaded_file(local_path, video):

                item = Item.objects.create(
                    name=video._name,
                    content_type=video.content_type,
                    project=project
                )

                process = multiprocessing.Process(target=upload_video_file, args=(local_path, item))
                process.start()

    context = {
        'title': 'Procesar nuevo vídeo',
        'form': UploadFileForm()
    }
    
    return render(request, 'items/create.html', context)


def handle_uploaded_file(local_path, video):
    with open(local_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)
    
    return local_path
