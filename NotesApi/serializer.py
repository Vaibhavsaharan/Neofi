from rest_framework import serializers, validators
from .models import Note, VersionHistory

class VersionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=VersionHistory
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        # Horrible hack - In order to reuse all other validation logic in the model field, we need to
        # remove the Uniqueness validation. This is ok because on create we'll first check
        # if the attribute already exists / is unique.
        new_validators = filter(
            lambda validator: not isinstance(validator, validators.UniqueValidator),
            self.fields["id"].validators
        )
        self.fields["id"].validators = new_validators
    
    class Meta:
        model=Note
        fields = '__all__'


class NoteSerializerValidated(serializers.ModelSerializer):    
    class Meta:
        model=Note
        fields = '__all__'