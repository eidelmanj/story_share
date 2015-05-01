from django.contrib import admin
from .models import Language, Country, Region, OwnedAudioFile, City, Dialect

# Register your models here.
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Dialect)
admin.site.register(OwnedAudioFile)
