from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect

from AWS import put_object

from .models import Item
from .forms import UploadFileForm
from .tasks import upload_video_file

from projects.models import Project

def create(request):
    form = UploadFileForm(request.POST or None)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.cleaned_data['file']
            name = video._name.split('.')[0].lower().replace(' ', '_')

            project = Project.objects.last() #create_by_aws(settings.BUCKET, name)
            
            local_path = f'tmp/{video._name}'
            if handle_uploaded_file(local_path, video):

                item = Item.objects.create(
                    name=video._name,
                    content_type=video.content_type,
                    project=project
                )

                upload_video_file.apply_async(args=(local_path, item.id))
                return redirect('projects:detail', project.id)

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
