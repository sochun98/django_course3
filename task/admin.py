from django.contrib import admin
import xlrd
from task.forms import StockUploadForm
from task.models import OutOfStock, Payment, Profit, Return, ReturnList, Set, StockUpload, Todo
from django.db.models import Q


admin.site.site_header = "Pharmacy Management"


@admin.action(description="제품 전체개수, 전체가격, 누적가격 계산하기")
def total_quantity_price(modeladmin, request, queryset):
    cum_price = 0
    for row in queryset:
        spec_num = row.spec_num or 0
        unit_num = row.unit_num or 0
        spec = row.spec or 1
        
        total_quantity = spec * spec_num + unit_num
        total_price = total_quantity * (row.unit_price or 0)
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
        spec = str(int(row.spec)) if row.spec is not None else "0"
        spec_num_str = str(int(row.spec_num)) if row.spec_num is not None else "0"
        unit_num_str = str(float(row.unit_num)) if row.unit_num is not None else "0"
        expiry_str = str(int(row.expiry)) if row.expiry is not None else "0"
        
        processed_row = f"{row.name} : {spec_num_str} (통/박스 [{spec}] ), {unit_num_str} (개/낱개), 유효기간 : {expiry_str}"
        data.append(processed_row)
        company = row.company
    
    combined_data = ", \n".join(data)
    
    content = f"안녕하세요 더샵참약국입니다.\n{combined_data}\n반품부탁드립니다 감사합니다!"
    
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
    modeladmin.message_user(request, f"전체수익 : {sum_margin}, 평균수익 : {average_margin}, 전체조제료 : {sum_presc}, 평균조제료 : {average_presc}, 전체매출 : {sum_otc}, 평균매출 : {average_otc}, 평균조제건수 : {average_presc_num}, 평균매출건수 : {average_otc_num}")
    

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


@admin.action(description="잔고금액 계산하기")
def balance_calc(modeladmin, request, queryset):
    i = 0
    for row in queryset:
        if i == 0:
            balance_temp = int(row.balance)
            i += 1
        else:
            balance = int(row.balance)
            stock = int(row.stock)
            payment = int(row.payment)
            balance = stock - payment + balance_temp
            payments = Payment.objects.filter(Q(id=row.id))
            for payment in payments:
                payment.balance = balance
                payment.save()
                balance_temp = balance
            i += 1


@admin.action(description="재고, 결제, 합계 구하기")
def sum_calc(modeladmin, request, queryset):
    # days = len(queryset)
    sum_stock = 0
    sum_payment = 0
    for row in queryset:
        sum_stock += row.stock
        sum_payment += row.payment

    modeladmin.message_user(request, f"재고합계 : {sum_stock}, 결제합계 : {sum_payment}")
            

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


@admin.action(description="입고현황 업로드")
def process_files(modeladmin, request, queryset):
    for obj in queryset:
        if obj.file:
            try:
                workbook = xlrd.open_workbook(file_contents=obj.file.read())
                sheet = workbook.sheet_by_index(0)
                
                for row in range(sheet.nrows):
                    if sheet.row_values(row)[0] != '입고일자':
                        date = int(sheet.row_values(row)[0].replace('-', ''))
                        company = sheet.row_values(row)[2]
                        stock = int(sheet.row_values(row)[3].replace(',', ''))
                        
                        payments = Payment.objects.filter(
                            Q(date=date) &
                            Q(company=company) &
                            Q(stock=stock)
                        )
                        
                        if not payments.exists():
                            Payment(date=date, company=company, stock=stock).save()
                            # print("새로운 입고장이 작성되었습니다.")
                
                modeladmin.message_user(request, "파일 처리가 완료되었습니다.")

            except Exception as e:
                modeladmin.message_user(request, f"오류 발생: {str(e)}", level='ERROR')


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
