import json
from typing import List
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class VersionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    editorId = models.UUIDField()
    addedLines = models.TextField()
    editedLines = models.TextField()
    tmsUpdate = models.IntegerField()

    def set_edited_lines(self, value):
        # Serialize the list to JSON before saving
        self.editedLines = json.dumps(value)

    def get_edited_lines(self):
        # Deserialize the JSON when retrieving the value
        return json.loads(self.editedLines)
    
    def set_added_lines(self, value):
        # Serialize the list to JSON before saving
        self.addedLines = json.dumps(value)

    def get_added_lines(self):
        # Deserialize the JSON when retrieving the value
        return json.loads(self.addedLines)


class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=50, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True)
    creatorId = models.CharField(max_length=50, blank=True)
    historyIds = models.TextField(blank=True)
    sharedUserIds = models.TextField(blank=True)
    tmsCreate = models.IntegerField()
    tmsUpdate = models.IntegerField()

    def set_shared_user_ids(self, value):
        # Serialize the list to JSON before saving
        self.sharedUserIds = json.dumps(value)

    def get_shared_user_ids(self):
        # Deserialize the JSON when retrieving the value
        return json.loads(self.sharedUserIds)
    
    def set_history_ids(self, value):
        # Serialize the list to JSON before saving
        self.historyIds = json.dumps(value)

    def get_history_ids(self) -> List:
        # Deserialize the JSON when retrieving the value
        return json.loads(self.historyIds)
    
