from django.contrib import admin
import xlrd
from task.actions import average_calc, balance_calc, price_sell_calc, process_files, product_return, profit_calc, sum_calc, total_quantity_price
from task.forms import StockUploadForm
from task.models import OutOfStock, Payment, Profit, Return, ReturnList, Set, StockUpload, Todo


admin.site.site_header = "Pharmacy Management"


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = [
        'entry', 'recall', 'completion', 'name', 'company', 'total_quantity', 'total_price', 'cum_price',
    ]
    fields = [
        'company', 'name', 'entry', 'recall', 'completion', 'code', 'spec', 'lot', 'expiry', 'spec_num', 'unit_num', 'unit_price',
    ]
    list_filter = ['company']
    search_fields = ['name', 'company', ]
    actions = [total_quantity_price, product_return]
    # total_quantity = spec * spec_num + unit_num
    # total_price = total_quantity * unit_price
    

@admin.register(ReturnList)
class ReturnListAdmin(admin.ModelAdmin):
    list_display = [
        'company', 'datetime', 
    ]
    fields = ['company', 'content',]
    list_filter = ['company']
    search_fields = ['datetime', 'company', 'content',]


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'comp1', 'comp2', 'comp3', 'price_sum', 'price_sell',
    ]
    fields = [
        'name', 'comp1', 'comp2', 'comp3', 'price1', 'price2', 'price3', 'price_sum', 'price_sell', 'code', 'content',
    ]
    search_fields = ['comp1', 'comp2', 'comp3',]
    actions = [price_sell_calc]


@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'margin_sum', 'presc_sum', 'otc_in', 'presc_num', 'otc_num',
    ]
    fields = [
        'date', ('bill_10k', 'bill_5k', 'bill_1k'), ('otc_discount', 'otc_margin'), 'amount_billing', ('presc_num', 'otc_num'), ('presc_in', 'presc_bill', 'presc_card'), ('otc_in', 'otc_bill', 'otc_card'), ('medicine_insur', 'medicine_nonsur'), ('presc_insur', 'presc_nonsur'), 'card_in', 'bill', 'presc_sum', ('presc_calc', 'otc_calc'), ('bill_calc', 'card_calc'), ('presc_gap', 'otc_gap'), ('card_gap', 'bill_gap'),
    ]
    actions = [profit_calc, average_calc]
    list_per_page = 27


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = [
        'must', 'datetime', 'checkbox',
    ]
    fields = [
        'must', 'checkbox',
    ]
    search_fields = ['must']
    list_filter = ['checkbox']


@admin.register(OutOfStock)
class OutOfStockAdmin(admin.ModelAdmin):
    list_display = [
        'datetime', 'name', 'stock',
    ]
    fields = [
        'name', 'stock',
    ]
    search_fields = ['name']
    list_filter = ['stock']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'company', 'stock', 'payment', 'balance', 'card',
    ]
    fields = [
        'date', 'company', 'stock', 'payment', 'card', 'balance',
    ]
    list_filter = [
        'company', 'card',
    ]
    search_fields = ['company', 'card']
    actions = [balance_calc, sum_calc]


@admin.register(StockUpload)
class StockUploadAdmin(admin.ModelAdmin):
    form = StockUploadForm
    list_display = ['file', 'uploaded_at']
    actions = [process_files]
    
    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('file')
        if files:
            for f in files:
                instance = StockUpload(file=f)
                instance.save()
        else:
            super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if obj.file:
            obj.file.delete(save=False)
        obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
        queryset.delete()
