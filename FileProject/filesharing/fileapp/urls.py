from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, upload_file, view_files, search_files, share_file, download_file, logout, delete_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('', view_files, name='view_files'),
    path('upload/', upload_file, name='upload_file'),
    path('search/', search_files, name='search_files'),
    path('share/<str:share_link>/', share_file, name='share_file'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]
# This allows serving uploaded media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)