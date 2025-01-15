from django.contrib import admin

from api.models import VPS


@admin.register(VPS)
class VPSAdmin(admin.ModelAdmin):
    list_display = ["uid", "ram", "hdd", "cpu", "status"]
    search_fields = ["uid"]
    list_display_links = ["uid"]


admin.site.site_header = "VPS Administration"
