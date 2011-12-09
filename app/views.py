from django.forms.fields import FileField
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.views.generic.list import ListView
from app.models import Authorizer, LogRecord
import logging
from M2Crypto.X509 import  load_cert_string
import base64

log = logging.getLogger(__name__)

class LogView(ListView):
    context_object_name = "log_list"
    template_name = "log.html"
    def get_queryset(self):
        user = get_object_or_404(Authorizer, name = self.args[0])
        records = LogRecord.objects.filter(who=user)
        return records
    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        context['subject'] = self.args[0]
        return context

class ScanView(View):

    def post(self, *args, **kwargs):
        try:
            subject = str(self.request.POST['subject'])
            content = str(self.request.POST['content'])
            nonce = str(self.request.POST['nonce'])
            signature = str(self.request.POST['signature'])

            log.debug("Subject=%s" % subject)
            log.debug("Content=%s" % content)
            log.debug("nonce=%s" % nonce)
            log.debug("signature=%s" % signature)

            qs = Authorizer.objects.filter(name = subject)

            if not qs.exists():
                log.info("Unable to find authorizer %s for resource %s" % (subject, content))
                return HttpResponseForbidden("Forbidden")

            cert = str(qs[0].cert)

            log.debug("Certificate: " + cert)

            try:
                result = self._verify(cert, content, nonce, signature)
            except Exception, e:
                log.error(e)
                return HttpResponseForbidden("Forbidden")

            if result != 1:
                return HttpResponseForbidden("Forbidden")

            record = LogRecord()
            record.who = qs[0]
            record.what = content
            record.save()

        except KeyError:
            return HttpResponseNotFound("Not Found")

        return HttpResponse('ok')

    def _verify(self, cert, content, nonce, signature):

        decodeSign = base64.b64decode(signature)

        c = load_cert_string(cert)

        log.debug("Successfully loaded cert")

        k = c.get_pubkey()

        k.verify_init()

        data = content+nonce

        k.verify_update(data)

        log.debug("Finished verify update")

        result = k.verify_final(decodeSign)

        log.debug("Finished verify final, result = %d" % result)

        return result



class AuthorizorView(View):

    def post(self, *args, **kwargs):
        try:
            subject = str(self.request.POST['subject'])
            content = str(self.request.POST['content'])
            nonce = str(self.request.POST['nonce'])
            signature = str(self.request.POST['signature'])

            log.debug("Subject=%s" % subject)
            log.debug("Content=%s" % content)
            log.debug("nonce=%s" % nonce)
            log.debug("signature=%s" % signature)

            # This should only return one item since the name is unique
            qs = Authorizer.objects.filter(name = subject, resource__name = content)

            if not qs.exists():
                log.info("Unable to find authorizer %s for resource %s" % (subject, content))
                return HttpResponseForbidden("Forbidden")

            cert = str(qs[0].cert)

            log.debug("Certificate: " + cert)

            try:
                result = self._verify(cert, content, nonce, signature)
            except Exception, e:
                log.error(e)
                return HttpResponseForbidden("Forbidden")

            if result != 1:
                return HttpResponseForbidden("Forbidden")

        except KeyError:
            return HttpResponseNotFound("Not Found")

        return HttpResponse('ok')

    def _verify(self, cert, content, nonce, signature):

        decodeSign = base64.b64decode(signature)

        c = load_cert_string(cert)

        log.debug("Successfully loaded cert")

        k = c.get_pubkey()

        k.verify_init() 

        data = content+nonce

        k.verify_update(data)

        log.debug("Finished verify update")

        result = k.verify_final(decodeSign)

        log.debug("Finished verify final, result = %d" % result)

        return result



class RegisterView(View):

    def post(self, *args, **kwargs):
        try:
            subject = str(self.request.POST['subject'])
            cert = str(self.request.POST['cert'])

            # Don't allow duplicate authorizers
            qs = Authorizer.objects.filter(name = subject)

            if qs.exists():
                return HttpResponseForbidden("Forbidden")

            log.info("Registering new Subject: %s" % subject)
            log.debug("Cert: %s" % cert)

            a = Authorizer()
            a.name = subject
            a.cert = cert
            a.save()

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


