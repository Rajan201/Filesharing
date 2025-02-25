# Register your models here.
from django.contrib import admin
from .models import FileUpload

@admin.register(FileUpload)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'file', 'uploaded_at')
