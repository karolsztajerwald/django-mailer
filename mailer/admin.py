from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse

from mailer.models import Message, DontSendEntry, MessageLog

import base64
import pickle


def show_to(message):
    return ", ".join(message.to_addresses)
show_to.short_description = "To"  # noqa: E305


class MessageAdminMixin(object):

    def plain_text_body(self, instance):
        email = instance.email
        if hasattr(email, 'body'):
            return email.body
        else:
            return "<Can't decode>"


class MessageAdmin(MessageAdminMixin, admin.ModelAdmin):

    list_display = ["id", show_to, "subject", "when_added", "priority", "title", "to_address"]
    readonly_fields = ['plain_text_body']
    date_hierarchy = "when_added"


class DontSendEntryAdmin(admin.ModelAdmin):

    list_display = ["to_address", "when_added"]


class MessageLogAdmin(MessageAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/messagelog_change_form.html"
    list_display = [
        "id", show_to, "subject", "message_id", "when_attempted", "result",
        "title", "to_address",
    ]
    list_filter = ["result"]
    date_hierarchy = "when_attempted"
    readonly_fields = ['plain_text_body', 'message_id']
    search_fields = ['message_id']
    actions = ['show_message_data']

    def show_message_data(self, request, queryset):
        data = ''
        for message in queryset:
            data += pickle.loads(base64.b64decode(message.message_data)).body
        return HttpResponse(data)
    show_message_data.short_description = 'Show message data'

    def get_urls(self):
        urls = super(MessageLogAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^show_message_data/(?P<message_id>\d+)/$', self.message_data, name="show_message_data")
        )
        return my_urls + urls

    def message_data(self, request, message_id):
        queryset = MessageLog.objects.filter(id=message_id)
        return self.show_message_data(request, queryset)


admin.site.register(Message, MessageAdmin)
admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)

