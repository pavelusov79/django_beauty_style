from django.contrib import admin
from mainapp.models import Masters, Services, ActionsNews, Contacts, Portfolio, WorkDays

admin.site.register(Masters)
admin.site.register(Services)
admin.site.register(ActionsNews)
admin.site.register(Portfolio)
admin.site.register(WorkDays)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('date_field', 'time_field', 'service_choice', 'masters_choice')
    list_filter = ('date_field', 'masters_choice')
