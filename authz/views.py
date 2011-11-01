from django.forms.fields import FileField, CharField
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.views.generic.base import View
from authz.models import Authorizer
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
                return HttpResponseForbidden("Forbidden")

        except KeyError:
            return HttpResponseNotFound("Not Found")

        return HttpResponse('ok')

class RegisterView(View):

    def post(self, *args, **kwargs):
        try:
            subject = self.request.POST['subject']
            cert = self.request.POST['cert']

            # Don't allow duplicate authorizers
            qs = Authorizer.objects.filter(name = subject)

            if qs.exists():
                return HttpResponseForbidden("Forbidden")

            log.info("Registering new Subject: %s" % subject)
            log.debug("Cert: %s" % cert)

        except KeyError:
            return HttpResponseNotFound("Not Found")

        return HttpResponse('ok')


class CertUploadView(View):

    def post(self, *args, **kwargs):
        class UploadForm(Form):
#            subject = CharField()
            file = FileField()

        try:
            form = UploadForm(self.request.POST, self.request.FILES)
            print self.request.FILES['file']
            if form.is_valid():
                log.debug("Multipart flag: %s" % form.is_multipart())
                log.debug("Valid flag: %s" % form.is_valid())
                file = self.request.FILES['file']
                print "Filename: ", file.name
                print "File Size: ", file.size
                data = file.read()
                print data
            else:
                return HttpResponseNotFound("Invalid")

        except Exception,e:
            log.error(e)
            return HttpResponseNotFound("Invalid")

        return HttpResponse('ok')


