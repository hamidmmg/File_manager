import os

from django.db import models
from users.models import User


# class Object(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='files_dir')
#     name = models.CharField(max_length=100)
#     file_type = models.CharField(max_length=100)
#     size = models.CharField(max_length=200)
#     is_trashed = models.BooleanField(default=False)
#     created_time = models.TimeField(auto_now_add=True)
#     last_opened = models.TimeField
#     last_modified = models.TimeField
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#
#     def extension(self):
#         name, extension = os.path.splitext(self.file.name)
#         return extension

class Object(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=100)
    size = models.CharField(max_length=200)
    is_trashed = models.BooleanField(default=False)
    created_time = models.TimeField(auto_now_add=True)
    last_opened = models.TimeField(auto_now_add=True)
    last_modified = models.TimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_uploaded = models.BooleanField(default=False)


    def __str__(self):
        return self.name +"          ======================             "+ str(self.id)

