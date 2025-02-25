from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FileUpload
from .forms import SignupForm
from django.contrib.auth import login, authenticate
from django.http import FileResponse, Http404
import os

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('view_files')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        name = request.POST.get('name', file.name)

        if file:
            FileUpload.objects.create(user=request.user, file=file, name=name)
            return redirect('view_files')

    return render(request, 'upload.html')

@login_required
def view_files(request):
    files = FileUpload.objects.filter(user=request.user)
    return render(request, 'view_files.html', {'files': files})

@login_required
def search_files(request):
    query = request.GET.get('q', '')
    files = FileUpload.objects.filter(user=request.user, name__icontains=query) if query else []
    return render(request, 'search.html', {'files': files, 'query': query})

def share_file(request, share_link):
    file = get_object_or_404(FileUpload, share_link=share_link)
    return render(request, 'share_file.html', {'file': file})

@login_required
def download_file(request, file_id):
    file_obj = get_object_or_404(FileUpload, id=file_id)
    # Construct the correct file path
    file_path = file_obj.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_obj.file.name))
    else:
        raise Http404("File not found on the server")

@login_required
def logout(request):
    # Your code to display files
    return render(request, 'logout.html')

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(FileUpload, id=file_id, user=request.user)
    file.file.delete()  # Deletes the actual file from storage
    file.delete()  # Deletes the database entry
    return redirect('view_files')
