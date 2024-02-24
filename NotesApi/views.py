import ast
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note, VersionHistory
from .serializer import NoteSerializer, NoteSerializerValidated, VersionHistorySerializer
import time
import uuid
# Create your views here.



@login_required
@api_view(['GET'])
def getNote(request, id):
    note = Note.objects.filter(id=id).first()
    user_id = request.user.uuid
    serializer = NoteSerializerValidated(instance=note)
    if note:
        if str(user_id) == note.creatorId or str(user_id) in note.get_shared_user_ids():
            return Response(serializer.data, status=200)
        else:
            return Response({"status": "Failure", "reason": "You are not authorized to view this note."}, status=403)
    else:
        return Response({"status": "Failure", "reason": "Notes does not exist"}, status=404)

@login_required
@api_view(['POST'])
def postNote(request):
    user_id = request.user.uuid
    serializer = NoteSerializer(data=request.data)
    code = 200
    if serializer.is_valid():
        data = serializer.validated_data
        note_id = data['id']
        if note_id is not None and len(note_id) > 0:
            prev_note = Note.objects.filter(id=note_id).first()
            if prev_note:
                if str(user_id) == prev_note.creatorId or str(user_id) in prev_note.get_shared_user_ids():
                # Updating the note (PUT functionality)
                    prev_note_content = prev_note.content
                    new_note_content = data['content']
                    prev_lines = prev_note_content.split('.')
                    curr_lines = new_note_content.split('.')

                    edited_lines = []
                    added_lines = []
                    for i, (prev_line, curr_line) in enumerate(zip(prev_lines, curr_lines)):
                        if prev_line != curr_line:
                            edited_lines.append(prev_line + " @#to#@ " + curr_line)

                    if len(curr_lines) > len(prev_lines):
                        for i in range(len(prev_lines), len(curr_lines)):
                            added_lines.append(curr_lines[i])
                    
                    version_history = {
                        'id': uuid.uuid4(),
                        'editorId': user_id,
                        'editedLines': json.dumps(edited_lines),
                        'addedLines': json.dumps(added_lines),
                        'tmsUpdate': int(time.time())
                    }
                

                    history_serializer = VersionHistorySerializer(data=version_history)
                    history_id = ''
                    if history_serializer.is_valid():
                        history_serializer.save()
                        history_id = history_serializer.data['id']
                    else:
                        print(history_serializer.errors)

                    new_history_list = prev_note.get_history_ids()
                    new_history_list.append(history_id)
                    data['tmsUpdate'] = int(time.time())
                    data['tmsCreate'] = prev_note.tmsCreate
                    data['sharedUserIds'] = prev_note.sharedUserIds
                    data['historyIds'] = json.dumps(new_history_list)
                    new_serializer = NoteSerializer(instance=prev_note, data=data, partial=True)

                    if new_serializer.is_valid():
                        new_serializer.save()
                else:
                    return Response({"status": "Failed", "reason": "You are not authorized to edit note"}, status=403)
            else:
                return Response({"status": "Failed", "reason": "Note does not exist"}, status=404)
        else:
            # Saving the note for first time (POST functionality)
            data['creatorId'] = user_id
            data['id'] = uuid.uuid4()
            note_id = data['id']
            data['tmsCreate'] = int(time.time())
            data['tmsUpdate'] = int(time.time())
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
            
            code = 201
        return Response({"status": "Success", "id": note_id}, status=code)
    else:
        print(serializer.errors)
        return Response({"status": "Failed", "reason": "Note object failed to serialize"})

@login_required
@api_view(['POST'])
def shareNote(request):
    # To share note with other users
    data = request.data
    user_id = request.user.uuid
    note_id = data['id']
    
    user_ids = ast.literal_eval(data['user_ids'])
    note = Note.objects.filter(id=note_id).first()
    if note:
        if str(user_id) == str(note.creatorId):
            shared_user_ids = list(set(user_ids + note.get_shared_user_ids()))
            data = NoteSerializerValidated(note).data
            data['sharedUserIds'] = json.dumps(shared_user_ids)
            serializer = NoteSerializerValidated(instance=note, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Success"}, status=200)
            else:
                return Response({"status": "Failed", "reason": "Failed to save note"}, status=500)
        else:
            return Response({"status": "Failed", "reason": "User is not authorized to share"})
    else:
        return Response({"status": "Failed", "reason": "Note does not exist"})


@login_required
@api_view(['GET'])
def getVersionHistory(request, note_id):
    user_id = request.user.uuid
    note = Note.objects.filter(id = note_id).first()
    if note:
        if note_id is not None and len(note_id) > 0 \
        and (str(user_id) == note.creatorId or str(user_id) in note.get_shared_user_ids()):

            note_histories = [VersionHistory.objects.filter(id=i).first() for i in note.get_history_ids() ]           
            serialized_data = []
            for obj in note_histories:
                serializer = VersionHistorySerializer(instance=obj)
                serialized_data.append(serializer.data)
            return Response(serialized_data, status=200)
        else:
            return Response({"status": "Failed", "reason": "Your are not authorized to get version history"}, status=403)
    else:
        return Response({"status": "Failed", "reason": "Note does not exist"}, status=404)
