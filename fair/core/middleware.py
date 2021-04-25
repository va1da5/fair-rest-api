from django.conf import settings
from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string


class RestAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user

        auth_modules = settings.REST_FRAMEWORK.get("DEFAULT_AUTHENTICATION_CLASSES")
        if not auth_modules:
            return request.user

        for module in auth_modules:
            auth_module = import_string(module)()
            try:
                user, _ = auth_module.authenticate(request)
                if user is not None:
                    return user
            except:
                pass

        return request.user

    def __call__(self, request):
        request.user = self.get_user(request)
        response = self.get_response(request)
        return response
