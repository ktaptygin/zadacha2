from django.contrib import admin
from .models import (
    Booking,
    Contact,
    DeliciousCategory,
    Delicious,
    Event,
    Speciality,
    StaticSection,
    UserProfile
)

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'people', 'date', 'time')
    list_filter = ('date', 'people')
    search_fields = ('name', 'email', 'phone')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')

admin.site.register(DeliciousCategory)
admin.site.register(Delicious)
admin.site.register(Event)
admin.site.register(Speciality)
admin.site.register(StaticSection)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')