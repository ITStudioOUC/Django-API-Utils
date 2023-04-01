from django.conf import settings
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        csrf_exempt_path_list = getattr(settings, 'CSRF_EXEMPT_PATH_LIST', ['all'])
        if csrf_exempt_path_list == ['all']:
            pass
        elif request.path in csrf_exempt_path_list:
            pass
        else:
            super().enforce_csrf(request)
