from pathlib import Path

from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse
from django.http import FileResponse

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404

from AWS import download_file

from .models import Item
from .common import get_lenguage
from .forms import UploadFileForm

from .tasks import delete_file
from .tasks import start_transcribe_and_translate

from projects.models import Project

@csrf_exempt
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    return JsonResponse({
            'id': item.id,
            'name': item.name,
            'delete_url': reverse('items:delete', kwargs={'pk': item.id})
        }
    )

def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    project = item.project
    
    item.delete()

    return redirect('projects:detail', project.id)
 
def download(request, pk):
    item = get_object_or_404(Item, pk=pk)

    local_path = f'tmp/{item.name}'
    Path('tmp/').mkdir(parents=True, exist_ok=True)
    
    if download_file(item.bucket, item.key, local_path):
        delete_file.apply_async(args=(local_path,), eta=timezone.now() + timedelta(minutes=1))
        return FileResponse(open(local_path, 'rb'))

    raise Http404

def create(request):
    form = UploadFileForm(request.POST or None)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.cleaned_data['file']
            name = video._name.strip().split('.')[0].lower().replace(' ', '_')

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
