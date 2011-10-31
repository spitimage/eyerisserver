from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.views.generic.base import View
from models import Authorizer
from models import Resource
import logging

log = logging.getLogger(__name__)

class AuthorizorView(View):

    def post(self, *args, **kwargs):
        try:
            subject = self.request.POST['subject']
            content = self.request.POST['content']
            nonce = self.request.POST['nonce']
            signature = self.request.POST['signature']

            log.info("Subject=%s" % subject)
            log.info("Content=%s" % content)
            log.info("nonce=%s" % nonce)
            log.info("signature=%s" % signature)

            # This should only return one item since the name is unique
            qs = Resource.objects.filter(name = content, authorizers__name = subject)

            if not qs.exists():
                return HttpResponseForbidden()

        except KeyError:
            return HttpResponseNotFound()

        return HttpResponse('ok')


