from django.contrib import admin
from .models import Note, VersionHistory

# Register your models here.
admin.site.register(Note)
admin.site.register(VersionHistory)