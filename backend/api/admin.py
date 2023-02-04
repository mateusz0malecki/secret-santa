from django.contrib import admin
from .models import SantaUser, SantaGroup, SantaList

admin.site.register(SantaUser)
admin.site.register(SantaGroup)
admin.site.register(SantaList)
