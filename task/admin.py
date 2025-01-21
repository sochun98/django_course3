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
        processed_row = row.name + ' : ' + str(int(row.spec_num)) + ' (통/박스 ), ' + str(int(row.unit_num)) + ' (개/낱개), 유통기한 : ' + str(int(row.expiry))
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


@admin.action(description="조제판매수익 계산하기")
def profit_calc(modeladmin, request, queryset):
    for row in queryset:
        bill = 10000*row.bill_10k + 5000*row.bill_5k + 1000*row.bill_1k
        presc_sum = row.presc_insur + row.presc_nonsur
        otc_margin = row.otc_margin
        presc_calc = bill + row.presc_card + row.otc_card + row.otc_discount + row.amount_billing - (row.otc_in + row.medicine_insur + row.medicine_nonsur)
        otc_calc = row.otc_card + row.otc_bill + row.otc_discount
        bill_calc = row.presc_in + row.otc_in - (row.presc_card + row.otc_card + row.otc_discount)
        card_calc = row.presc_card + row.otc_card
        otc_in = row.otc_in
        card_in = row.card_in
        
        profits = Profit.objects.filter(date__contains=row.date)
        if profits.exists():
            for profit in profits:
                profit.presc_sum = presc_sum
                profit.margin_sum = presc_sum + otc_margin
                profit.presc_calc = presc_calc
                profit.otc_calc = otc_calc
                profit.bill_calc = bill_calc
                profit.card_calc = card_calc
                profit.bill = bill
                profit.presc_gap = presc_sum - presc_calc
                profit.otc_gap = otc_in - otc_calc
                profit.card_gap = card_in - card_calc
                profit.bill_gap = bill - bill_calc
                profit.save()
        modeladmin.message_user(request, "조제판매수익 계산이 완료되었습니다.")


@admin.action(description="평균수익 계산하기")
def average_calc(modeladmin, request, queryset):
    days = len(queryset)
    sum_margin = 0
    sum_presc = 0
    sum_otc = 0
    sum_presc_num = 0
    sum_otc_num = 0
    for row in queryset:
        sum_margin += row.margin_sum
        sum_presc += row.presc_sum
        sum_otc += row.otc_in
        sum_presc_num += row.presc_num
        sum_otc_num += row.otc_num
    average_margin = int(sum_margin / days)
    average_presc = int(sum_presc / days)
    average_otc = int(sum_otc / days)
    average_presc_num = int(sum_presc_num / days)
    average_otc_num = int(sum_otc_num / days)
    modeladmin.message_user(request, f"전체수익 : {sum_margin}, 평균수익 : {average_margin}, 평균조제료 : {average_presc}, 평균매출 : {average_otc}, 평균조제건수 : {average_presc_num}, 평균매출건수 : {average_otc_num}")
    

@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'margin_sum', 'presc_sum', 'otc_in', 'presc_num', 'otc_num',
    ]
    fields = [
        'date', 'bill_10k', 'bill_5k', 'bill_1k', 'otc_discount', 'otc_margin', 'amount_billing', 'presc_num', 'otc_num', 'presc_in', 'presc_bill', 'presc_card', 'otc_in', 'otc_bill', 'otc_card', 'medicine_insur', 'medicine_nonsur', 'presc_insur', 'presc_nonsur', 'card_in', 'bill', 'presc_sum', 'presc_calc', 'otc_calc', 'bill_calc', 'card_calc', 'presc_gap', 'otc_gap', 'card_gap', 'bill_gap',
    ]
    actions = [profit_calc, average_calc]