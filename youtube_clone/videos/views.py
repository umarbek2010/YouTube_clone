from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm

def home(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = VideoForm()

    return render(request, 'videos/upload.html', {'form': form})