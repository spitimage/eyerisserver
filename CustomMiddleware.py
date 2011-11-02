from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

class FilterSessionMiddleware(SessionMiddleware):
    '''
    This guy filters the session stuff out for anything but the admin page. If this
    site gets too complex, the correct solution is to have 2 WSGI instances.
    '''
    def process_request(self, request):
        if not request.path_info.startswith('/admin/'):
            return
        super(FilterSessionMiddleware, self).process_request(request)

    def process_response(self, request, response):
        if not request.path_info.startswith('/admin/'):
            return response
        return super(FilterSessionMiddleware, self).process_response(request, response)

class FilterAuthMiddleware(AuthenticationMiddleware):
    '''
    This guy filters the session stuff out for anything but the admin page. If this
    site gets too complex, the correct solution is to have 2 WSGI instances.
    '''
    def process_request(self, request):
        if not request.path_info.startswith('/admin/'):
            return
        super(FilterAuthMiddleware, self).process_request(request)


