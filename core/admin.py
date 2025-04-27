from django.contrib import admin
from .models import Species, Country, SGObservation, SGBird

admin.site.register(Species)
admin.site.register(Country)
admin.site.register(SGObservation)
admin.site.register(SGBird)