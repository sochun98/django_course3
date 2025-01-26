from decimal import Decimal
import decimal
from django.contrib import admin
import xlrd
from etc.forms import EtcUploadForm
from etc.models import Etc, EtcUpload, OrderList


@admin.action(description="제품 주문서 작성하기")
def product_order(modeladmin, request, queryset):
    data = []
    for row in queryset:
        processed_row = row.name + ' : ' + str(int(row.order)) + ' EA'
        data.append(processed_row)
        company = row.company
    
    combined_data = ", \n".join(data)
        
    content = '안녕하세요 더샵참약국입니다.\n\n' + combined_data + '\n\n주문할게요 감사합니다!'
    
    new_object = OrderList(company=company, content=content)
    new_object.save()
    print("주문서 작성이 완료되었습니다.")
        

@admin.register(Etc)
class EtcAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'quantity', 'target', 'order', 'expiry', 'get_ingredients',
    ]
    fields = [
        'company', 'name', 'target', 'order', 'expiry', 'old_expiry', 'ingredients', 'effects', 'dosage', 'precautions', 
        ]
    filter_horizontal = ['ingredients'] # 다대다 관계를 위한 편리한 인터페이스
    list_filter = ['order', ]
    search_fields = [
        'name', 'company', 'ingredients_name', 'effects', 
    ]
    actions = [product_order]
    
    def get_ingredients(self, obj):
        return ", ".join([i.name for i in obj.ingredients.all()])
    get_ingredients.short_description = '성분'


@admin.action(description="조제약품 재고 최신화")
def etc_update(modeladmin, request, queryset):
    for obj in queryset:
        if obj.file:
            try:
                workbook = xlrd.open_workbook(file_contents=obj.file.read())
                sheet = workbook.sheet_by_index(0)
                
                for row in range(sheet.nrows):
                    if sheet.row_values(row)[0] != '약품명':
                        product_name = sheet.row_values(row)[0]
                        # product_code = sheet.row_values(row)[1]
                        product_company = sheet.row_values(row)[3]
                        # product_price = sheet.row_values(row)[4]
                        
                        try:
                            value = sheet.row_values(row)[7]
                            value = value.strip().replace(',', '').replace(' ', '')
                            decimal_number = Decimal(value)
                        except decimal.InvalidOperation as e:
                            print(f"값 '{value}'에 대해 유효하지 않은 소수 연산이 발생했습니다, 행 {row + 1}: {e}")
                            decimal_number = Decimal('0')
                        except ValueError as e:
                            print(f"'{value}' 값에 대한 오류, 행 {row + 1}: {e}")
                            decimal_number = Decimal('0')
                            
                        product_quantity = decimal_number
                        
                        etcs = Etc.objects.filter(name__contains=product_name)
                        
                        if etcs.exists():
                            for etc in etcs:
                                if len(etc.name) == len(product_name):
                                    etc.quantity = product_quantity
                                    etc.order = etc.target - product_quantity
                                    etc.save()
                        else:
                            product_target = 0
                            product_order = product_target - product_quantity
                            new_object = Etc(name=product_name, company=product_company, quantity=product_quantity, target=product_target, order=product_order)
                            new_object.save()
                            print("새로운 품목이 추가되었습니다.")
    
                print("재고 최신화가 완료되었습니다.")

                modeladmin.message_user(request, "조제약품 재고 최신화 되었습니다.")
            except Exception as e:
                modeladmin.message_user(request, f"Error reading file '{obj.file.name}': {str(e)}", level='error')
        else:
            modeladmin.message_user(request, f"No file uploaded for '{obj}'.", level='warning')


@admin.register(EtcUpload)
class EtcUploadAdmin(admin.ModelAdmin):
    form = EtcUploadForm
    actions = [etc_update]
    list_display = ('get_file_name',)
    
    def get_file_name(self, obj):
        return obj.file.name
    get_file_name.short_description = '파일 이름'
    
    def delete_model(self, request, obj):
        if obj.file:
            obj.file.delete(save=False)
        obj.delete()
    
    def dlelte_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
        queryset.delete()


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = [
        'company', 'datetime', 
    ]
    fields = ['company', 'content', ]
    list_filter = ['company']
    search_fields = ['datetime', 'company', 'content', ]