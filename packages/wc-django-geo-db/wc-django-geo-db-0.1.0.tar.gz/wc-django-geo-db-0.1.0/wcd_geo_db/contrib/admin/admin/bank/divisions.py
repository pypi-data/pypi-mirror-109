from django.contrib import admin

from wcd_geo_db.modules.bank.db import Division


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'level', 'path', 'types'
    list_filter = 'level',
    search_fields = 'name', 'types', 'codes'
