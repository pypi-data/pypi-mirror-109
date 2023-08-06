from django.conf import settings
from django.urls import reverse


class DjangoSamonBinding:
    def url(self, view_name, *args, **kwargs):
        return reverse(view_name, args=args, kwargs=kwargs)


def djsamon(request):
    return {
        'djsamon': DjangoSamonBinding()
    }
