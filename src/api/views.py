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


from django.http import HttpResponse
from django.template import loader


class VideoSearchMixin:
    def __init__(self, **kwargs) -> None:
        self.queryset = YoutubeData.objects
        super().__init__(**kwargs)

    def paginate(self, limit, page):
        offset = limit * page
        self.queryset = self.queryset[offset:limit]

    def filter_q(self, q_str):
        all_fields = [f.name for f in YoutubeData._meta.fields]
        self.queryset = (
            self.queryset.annotate(
                search=SearchVector("title") + SearchVector("description")
            )
            .filter(search=SearchQuery(q_str))
            .values(*all_fields)
        )


class VideoAPIWeb(VideoSearchMixin, View):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def paginate_qp(self, request):
        limit = int(request.POST.get("limit", 10))
        page = int(request.POST.get("page", 0))
        self.paginate(limit=limit, page=page)
        return page

    def filter_qp(self, request):
        q_str = request.POST.get("q", "")
        if not q_str:
            self.queryset = self.queryset.values()
            return
        self.filter_q(q_str=q_str)

    def get(self, request):
        template = loader.get_template("search.html")
        context = {"data": []}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        self.filter_qp(request)
        self.paginate_qp(request)
        template = loader.get_template("search.html")
        context = {
            "data": list(self.queryset),
        }
        return HttpResponse(template.render(context, request))


class VideoAPI(VideoSearchMixin, View):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def paginate_qp(self, request):
        limit = int(request.GET.get("limit", 10))
        page = int(request.GET.get("page", 0))
        self.paginate(limit=limit, page=page)
        return page

    def filter_qp(self, request):
        q = request.GET.getlist("q", [])
        if not q:
            self.queryset = self.queryset.values()
            return
        q_str = " ".join(q)
        self.filter_q(q_str=q_str)

    def get(self, request):
        page = self.filter_qp(request)
        self.paginate_qp(request)
        data = list(self.queryset)
        return JsonResponse(
            data={"count": len(data), "page": page, "data": data}, safe=False
        )
