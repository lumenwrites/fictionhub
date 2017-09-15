from django.contrib import admin

from .models import Source


class SourceAdmin(admin.ModelAdmin):
    search_fields = ['url']

admin.site.register(Source, SourceAdmin)

