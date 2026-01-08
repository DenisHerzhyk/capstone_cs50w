from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('upload/', views.upload_images, name='upload_images'),
    path('file_generation_in_progress/', views.file_generation_in_progress, name='file_generation_in_progress'),
    path('get_generated_file/', views.get_generated_file, name='get_generated_file')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)