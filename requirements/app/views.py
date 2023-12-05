from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.serializer import AudioListSerializer
from app.models import AudioList
import os
from django.core.exceptions import ValidationError


class CreatView(GenericAPIView):
   
    serializer_class = AudioListSerializer
    queryset = AudioList.objects.all()


    def get(self,request):
        
        queryset = AudioList.objects.all()
        serializer = AudioListSerializer(queryset, many=True)
        return Response(serializer.data)
        

    def post(self,request):
        serializer = AudioListSerializer(data=request.data)
        file = request.data['file_path']
        if file:
            # if file._size > 4*1024*1024:
            #     raise ValidationError("Audio file too large ( > 4mb )")

            # if not file.content-type in ["audio/mpeg","audio/wav"]:
            #     raise ValidationError("Content-Type is not mpeg")
            if not os.path.splitext(file.name)[1] in [".mp3",".wav",".wma", ".amr"]:
                raise ValidationError("Doesn't have proper extension")
                return file

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError("Couldn't read uploaded file")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailView(GenericAPIView):
    serializer_class = AudioListSerializer
    queryset = AudioList.objects.all()

    def get(self, request, id):
        queryset = AudioList.objects.get(id=id)
        serializer = AudioListSerializer(queryset)
        return Response(serializer.data)


    def put(self, request, id, format=None):
        queryset = AudioList.objects.get(id=id)
        serializer = AudioListSerializer(queryset, data=request.data)
        file = queryset.file_path
        if file:
            if not os.path.splitext(file.name)[1] in [".mp3",".wav",".wma", ".amr"]:
                raise ValidationError("Doesn't have proper extension")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        queryset = AudioList.objects.get(id=id)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
