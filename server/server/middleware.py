import re
from oauth2_provider.models import AccessToken
from rest_framework.authentication import BaseAuthentication
from functools import wraps
def add_info_user_middleware(get_response):
    @wraps(get_response)
    def middleware(request):
        app_tk = request.headers.get('Authorization')
        if app_tk is None:
            return get_response(request)
        m = app_tk.split(' ')
        app_tk = m[1]
        access_user = AccessToken.objects.get(token=app_tk)
        print(access_user.user_id, 'acc_tk')
        request.META['current_account_id'] = access_user.user_id
        return get_response(request)
    return middleware

class CustomMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        app_tk = request.headers.get('Authorization')
        response = self.get_response(request)
        if app_tk is None:
            return response
        m = app_tk.split(' ')
        app_tk = m[1]
        access_user = AccessToken.objects.get(token=app_tk)
        print(access_user.user_id, 'acc_tk')

        response.get_current_account = access_user.user_i
        return response
