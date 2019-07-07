from django.contrib import admin

from notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'message', 'created']
    list_filter = ['created']
    search_fields = ['title', 'message']

    date_hierarchy = 'created'


admin.site.register(Notification, NotificationAdmin)
