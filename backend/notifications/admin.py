from django.contrib import admin

from .models import  Message

class MessageAdmin(admin.ModelAdmin):
    search_fields = ['body']

admin.site.register(Message, MessageAdmin)
