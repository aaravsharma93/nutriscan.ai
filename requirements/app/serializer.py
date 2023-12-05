from rest_framework import serializers
from app.models import AudioList

class AudioListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AudioList
        fields = '__all__'