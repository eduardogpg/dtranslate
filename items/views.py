from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Item
from .common import get_lenguage
from .forms import UploadFileForm
from .tasks import start_transcribe_and_translate

from projects.models import Project

def create(request):
    form = UploadFileForm(request.POST or None)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.cleaned_data['file']
            name = video._name.split('.')[0].lower().replace(' ', '_').strip()

            project = Project.objects.create_by_aws(settings.BUCKET, settings.LOCATION, name)
            
            local_path = handle_uploaded_file(video)
            if local_path:

                target = get_lenguage(int(form.cleaned_data['target']))
                lenguage = get_lenguage(int(form.cleaned_data['lenguage']))

                item = Item.objects.create(
                    name=video._name,
                    content_type=video.content_type,
                    project=project,
                    lenguage=lenguage
                )

                start_transcribe_and_translate.apply_async(args=(local_path, item.id, target))
                return redirect('projects:detail', project.id)

    context = {
        'title': 'Procesar nuevo vídeo',
        'form': UploadFileForm()
    }
    
    return render(request, 'items/create.html', context)


def handle_uploaded_file(video):
    Path('tmp/').mkdir(parents=True, exist_ok=True)
    local_path = f'tmp/{video._name}'
    
    with open(local_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)
    
    return local_path
