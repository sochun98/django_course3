from django.contrib import admin
from task.models import Profit, Return, ReturnList, Set


@admin.action(description="제품 전체개수, 전체가격, 누적가격 계산하기")
def total_quantity_price(modeladmin, request, queryset):
    cum_price = 0
    for row in queryset:
        total_quantity = row.spec * row.spec_num + row.unit_num
        total_price = total_quantity * row.unit_price
        cum_price += total_price
        returns = Return.objects.filter(name__contains=row.name)
        if returns.exists():
            for product in returns:
                if product.entry == row.entry and product.expiry == row.expiry:
                    product.total_quantity = total_quantity
                    product.total_price = total_price
                    product.cum_price = cum_price
                    product.save()


@admin.action(description="제품 반품요청서 작성하기")
def product_return(modeladmin, request, queryset):
    data = []
    for row in queryset:
        processed_row = row.name + ' : ' + str(int(row.spec_num)) + ' (통/박스 ), ' + str(int(row.unit_num)) + ' (개/낱개)'
        data.append(processed_row)
        company = row.company
    
    combined_data = ", \n".join(data)
    
    content = '안녕하세요 더샵참약국입니다.\n' + combined_data + '\n반품부탁드립니다 감사합니다!'
    
    new_object = ReturnList(company=company, content=content)
    new_object.save()
    modeladmin.message_user(request, f"{company} 반품요청서 작성이 완료되었습니다.")
    print("반품요청서 작성이 완료되었습니다.")
    

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = [
        'entry', 'recall', 'completion', 'name', 'company', 'total_quantity', 'total_price', 'cum_price',
    ]
    fields = [
        'company', 'name', 'entry', 'recall', 'completion', 'code', 'spec', 'lot', 'expiry', 'spec_num', 'unit_num', 'unit_price',
    ]
    list_filter=['company']
    search_fields = ['name', 'company', ]
    actions = [total_quantity_price, product_return]
    # total_quantity = spec * spec_num + unit_num
    # total_price = total_quantity * unit_price
    

@admin.register(ReturnList)
class ReturnListAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'datetime', 'company',
    ]
    fields = ['company', 'content',]
    search_fields = ['datetime', 'company', 'content',]


@admin.action(description="세트상품 원가가격 계산")
def price_sell_calc(modeladmin, request, queryset):
    for row in queryset:
        # price_sum = int(row.price1) + int(row.price2) + int(row.price3)
        price_sum = row.price1 + row.price2 + row.price3
        sets = Set.objects.filter(name__contains=row.name)
        if sets.exists():
            for set in sets:
                set.price_sum = price_sum
                set.save()
    modeladmin.message_user(request, f"{row.name} 원가가격 계산이 완료되었습니다.")


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
        'date', 'bill_10k', 'bill_5k', 'bill_1k', 'otc_in', 'otc_discount', 'otc_margin', 'presc_num', 'otc_num', 'presc_in', 'presc_bill', 'presc_card', 'otc_bill', 'otc_card', 'medicine_insur', 'medicine_nonsur', 'presc_insur', 'presc_nonsur', 'card_in', 
    ]
