from django.contrib import admin
from authz.models import *

admin.site.register(Authorizer)
admin.site.register(Resource)
admin.site.register(LogRecord)

# TODO You can add a custom ModelAdmin class here for admin page customizations to your heart's content