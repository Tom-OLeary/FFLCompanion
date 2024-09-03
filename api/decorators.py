from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView


def require_token(func):
    def _check_auth(view, *args, **kwargs):
        if not view.request.user.is_authenticated:
            return Response(BaseAPIView.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return func(view, *args, **kwargs)

    return _check_auth
