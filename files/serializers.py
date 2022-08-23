from rest_framework import serializers
from .models import Object


class CreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    file_type = serializers.CharField(required=False)
    size = serializers.CharField(required=False)
    object_id = serializers.IntegerField(required=False)

    def validate(self, data):

        try:
            data['size']
        except:
            data['file_type'] = 'folder'
        if data['file_type'] == 'folder':
            try:
                array = Object.objects.filter(parent=data['object_id']).values_list('size')
                arrayd1 = []
                print(array)
                for i in array:
                    arrayd1.append(i[0])
                final_sum = 0
                for j in arrayd1:
                    final_sum += int(j)
                filesize = final_sum
                data['size'] = filesize
            except:
                data['size'] = 0
        else:
            try:
                parent = data['parent']
                obj = Object.objects.get(id=parent.id)
                obj_size = obj.size
                obj.size = obj_size+data['size']
                obj.save()
            except:
                pass
        return data

    class Meta:
        model = Object
        fields = ['name', 'size', 'file_type', 'parent', 'object_id']

# class CreateSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)
#     file_type = serializers.CharField(required=False)
#     size = serializers.CharField(required=False)
#     object_id = serializers.IntegerField(required=False)
#
#     def validate(self, data):
#
#         try:
#             data['size']
#         except:
#             data['file_type'] = 'folder'
#         if data['file_type'] == 'folder':
#             array = Object.objects.filter(parent=data['object_id']).values_list('size')
#             arrayd1 = []
#             print(array)
#             for i in array:
#                 arrayd1.append(i[0])
#             final_sum = 0
#             for j in arrayd1:
#                 final_sum += int(j)
#             filesize = final_sum
#             data['size'] = filesize
#         # try:
#         #     data['file_type']
#         # except:
#         #     raise serializers.ValidationError('inter file_type!')
#         return data
#
#     class Meta:
#         model = Object
#         fields = ['name', 'size', 'file_type', 'parent', 'object_id']


class UploadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Object
        fields = ['id', ]


class DeleteObjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Object
        fields = ['id', ]


class TrashObjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Object
        fields = ['id', ]


class GetObjectDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    class Meta:
        model = Object
        fields = ['id', ]
