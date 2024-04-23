
from rest_framework.generics import ListCreateAPIView
from .serializers import PhotoSerializer
from .models import Photo
from .tasks import predict_image  # Import your Celery task

class PhotoAPIView(ListCreateAPIView):
    queryset = Photo.objects.all().order_by('-id')
    serializer_class = PhotoSerializer
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        data = serializer.data
        predict_image.delay(data) 