from django.utils import timezone



class DailyVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_client_ip(request):
        return _.split(',')[0] if (_ := request.META.get('HTTP_X_FORWARDED_FOR')) else request.META.get('REMOTE_ADDR')

    @staticmethod
    def get_user(request):
        return (request.user.is_authenticated and request.user) or None

    def __call__(self, request):
        if  request.path in ["/user/verify_code/","/user/send_code/"]:
            request.custom_info = {
                "ip": self.get_client_ip(request),
            }
        response = self.get_response(request)
        return response