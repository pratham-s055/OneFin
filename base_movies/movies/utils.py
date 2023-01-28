from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def get_tokens_for_user(user):
    """
    Creates token for user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
    }



class RequestCounterMiddleware:
    request_count = 0
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.__class__.request_count += 1
        response = self.get_response(request)
        return response

    def reset_counter(self):
        self.__class__.request_count = 0



