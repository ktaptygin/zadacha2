from django.contrib import admin
from .models import (
    Booking,
    Contact,
    DeliciousCategory,
    Delicious,
    Event,
    Speciality,
    StaticSection,
)

# Register your models here.

admin.site.register(Booking)
admin.site.register(Contact)
admin.site.register(DeliciousCategory)
admin.site.register(Delicious)
admin.site.register(Event)
admin.site.register(Speciality)
admin.site.register(StaticSection)