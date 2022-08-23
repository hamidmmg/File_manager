from django.urls import path
from .views import CreateObjectAPIView, DeleteAPIView, TrashAPIView, GetProfileAPIVIew, GetObjectDetailAPIView, \
    UploadObjectAPIView

urlpatterns = [
    path('create/', CreateObjectAPIView.as_view()),
    path('upload/', UploadObjectAPIView.as_view()),
    path('delete/', DeleteAPIView.as_view()),
    path('trash/', TrashAPIView.as_view()),
    path('getprofile/', GetProfileAPIVIew.as_view()),
    path('getobject/', GetObjectDetailAPIView.as_view()),
]
