from django.contrib import admin

from .models import Series


class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    

admin.site.register(Series, SeriesAdmin)



