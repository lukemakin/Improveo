
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.http import Http404


class CustomMiddlewareExample(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = resolve(request.path).url_name
        if not ip == '127.0.0.1' and path == "posts:post-list":
            raise Http404("No acces for this user")
        else:
            print('this path is ok for this user')
            return None
