from django.urls import path

from . import views

app_name = 'FitMirror'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.ImageUploadView.as_view(), name='image-upload'),
]