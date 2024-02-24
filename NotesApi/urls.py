from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('get/<id>/', views.getNote),
    path('save/',views.postNote),
    path('share/', views.shareNote),
    path('version-history/<note_id>/',views.getVersionHistory),
]