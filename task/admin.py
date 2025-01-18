from django.contrib import admin
from task.models import Return


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = [
        'entry', 'recall', 'completion', 'name', 'company',
    ]
    fields = [
        'name', 'company', 'entry', 'recall', 'completion', 'code', 'spec', 'lot', 'expiry', 'spec_num', 'unit_num', 'unit_price', 'total_quantity', 'total_price',
    ]
    list_filter=['company']
    search_fields = ['name', 'company', ]
    # total_quantity = spec * spec_num + unit_num
    # total_price = total_quantity * unit_price