from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from lastfm import LastFM


class IndexView(View):
    lastfm = LastFM(settings.LASTFM_API_KEY)

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.POST.get('user')
        period = request.POST.get('period')
        # TODO: adicionar limit no front
        limit = request.POST.get('limit', 26)

        if not all([user, period, limit]):
            # TODO: criar página de erro
            return HttpResponseBadRequest('<h1>Parâmetros inválidos</h1>')

        collage = self.lastfm.gen_top_albums_collage(user, period, limit)
        response = HttpResponse(content_type='image/png')
        collage.save(response, 'PNG')

        return response
