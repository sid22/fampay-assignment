from django.http import JsonResponse
from api.models import YoutubeData

# Create your views here.


def get_video_data(request):
    filters = request.GET
    print("filters ", filters, type(filters))
    data = YoutubeData.objects.all()
    return JsonResponse(data={"key": "value"})
