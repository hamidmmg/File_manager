import os
import datetime
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateSerializer, DeleteObjectSerializer, TrashObjectSerializer, GetObjectDetailSerializer, \
    UploadSerializer
from .models import Object, User


# class CreateObjectAPIView(generics.CreateAPIView):
#     serializer_class = CreateSerializer
#     permission_classes = (IsAuthenticated, )
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         file = serializer.validated_data['file']
#         splited_name = file.name.split('.')
#         name = splited_name[0]
#         if splited_name[1]:
#             extension = splited_name[1]
#         else:
#             pass
#
#         filesize = file.size/1000
#         print('=================================')
#         print(file.size/1000)
#         print('=================================')
#         Object.objects.create(name=name, file_type=extension, file=file, user=user, size=filesize)
#         old_used = User.objects.get(id=user.id).used_storage
#         print(old_used)
#         User.objects.filter(id=user.id).update(used_storage=old_used+file.size/1000)
# return Response("file uploaded")

class CreateObjectAPIView(generics.CreateAPIView):
    serializer_class = CreateSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        filesize = serializer.validated_data['size']
        extension = serializer.validated_data['file_type']
        try:
            parent_id = serializer.validated_data['parent']
            Object.objects.create(name=name, file_type=extension, user=user, size=filesize, parent=parent_id)
        except:
            Object.objects.create(name=name, file_type=extension, user=user, size=filesize)
        return Response("object created")


class UploadObjectAPIView(generics.CreateAPIView):
    serializer_class = UploadSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        object_id = serializer.validated_data['id']
        if Object.objects.get(id=object_id).user == user:
            if not Object.objects.get(id=object_id).is_uploaded:
                obj = Object.objects.get(id=object_id)
                filesize = obj.size
                obj.is_uploaded = True
                obj.save()
                old_used = User.objects.get(id=user.id).used_storage
                User.objects.filter(id=user.id).update(used_storage=int(old_used) + int(filesize))
                print(old_used)
                return Response('item uploaded ! ')
            else:
                return Response('item already uploaded ! ')
        else:
            return Response('object not found! ')


class DeleteAPIView(APIView):
    serializer_class = DeleteObjectSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        object_id = serializer.validated_data['id']
        if Object.objects.get(id=object_id).user == user:
            freed_size = Object.objects.filter(id=object_id).first().size
            Object.objects.filter(id=object_id).delete()
            old_used = User.objects.get(id=user.id).used_storage
            User.objects.filter(id=user.id).update(used_storage=int(old_used) - int(freed_size))
            return Response('item deleted ! ')
        else:
            return Response('object not found! ')


class TrashAPIView(APIView):
    serializer_class = TrashObjectSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        object_id = serializer.validated_data['id']
        now = datetime.datetime.now()
        time = now.time()
        if not Object.objects.get(id=object_id).is_trashed:
            Object.objects.filter(id=object_id).update(is_trashed=True)
            obj = Object.objects.get(id=object_id)
            obj.last_modified = time
            obj.save()
            return Response('item Trashed ! ')
        else:
            return Response('The item has already been trashed !')


class GetProfileAPIVIew(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        old_used = User.objects.get(id=user.id).used_storage
        total_storage = User.objects.get(id=user.id).total_storage
        remain_storage = int(total_storage)-int(old_used)
        return Response({'old_used': old_used, 'remain_storage': remain_storage}, status=status.HTTP_200_OK)


class GetObjectDetailAPIView(APIView):
    serializer_class = GetObjectDetailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        object_id = serializer.validated_data['id']
        obj = Object.objects.get(id=object_id)
        now = datetime.datetime.now()
        time = now.time()
        obj.last_opened = time
        obj.save()
        if obj.user == user:
            file_type = obj.file_type
            size = obj.size
            name = obj.name
            add_date = obj.created_time
            opened_date = obj.last_opened
            modified = obj.last_modified
            print(modified)
            return Response({'name': name, 'file_type': file_type, 'size': size, 'add_date': add_date,
                             'opened_date': opened_date, 'last modified': modified}, status=status.HTTP_200_OK)
        else:
            return Response('entered object id is wrong !')
