from django.contrib import admin
from otc.models import Otc
from otc.models import ExcelUpload
from otc.forms import ExcelUploadForm


@admin.register(Otc)
class OtcAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'company', 'quantity', 'target', 'order',
    ]
    fields = ['name', 'company', 'code', 'quantity', 'target', 'order', ]
    list_filter = ['order', ]
    search_fields = ['name', 'company', ]


@admin.action(description="판매약품 재고 최신화")
def otc_update(modeladmin, request, queryset):
    

@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    form = ExcelUploadForm
    actions = [otc_update]

# admin.site.register(Otc, OtcAdmin)

# admin.site.register(ExcelUpload, ExcelUploadAdmin)