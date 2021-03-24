from django.contrib.postgres.search import SearchQuery, SearchVector
from django.http import JsonResponse
from django.views import View

from api.external import APIKeyHelper
from api.models import YoutubeData

# Create your views here.


def add_api_key(request):
    key = request.GET.get("api_key")
    APIKeyHelper.set_api_key(key=key)
    return JsonResponse(data={"message": "success"})


class VideoAPI(View):
    def __init__(self, **kwargs) -> None:
        self.queryset = YoutubeData.objects
        super().__init__(**kwargs)

    def paginate(self, request):
        limit = int(request.GET.get("limit", 10))
        page = int(request.GET.get("page", 0))
        offset = limit * page
        self.queryset = self.queryset[offset:limit]

    def filter_q(self, request):
        q = request.GET.getlist("q", [])
        if not q:
            self.queryset = self.queryset.values()
            return
        q_str = " ".join(q)
        all_fields = [f.name for f in YoutubeData._meta.fields]
        self.queryset = (
            self.queryset.annotate(
                search=SearchVector("title") + SearchVector("description")
            )
            .filter(search=SearchQuery(q_str))
            .values(*all_fields)
        )

    def get(self, request):
        self.filter_q(request)
        self.paginate(request)
        return JsonResponse(data=list(self.queryset), safe=False)
