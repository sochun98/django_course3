from decimal import Decimal, InvalidOperation
import decimal
import os
from django.contrib import admin, messages
import xlrd
from etc.forms import EtcUploadForm, RespiryRegistForm
from etc.models import Etc, EtcUpload, OrderList, RespiryRegist


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
        'company', 'name', 'code', 'price', 'target', 'order', 'expiry', 'old_expiry', 'ingredients', 'effects', 'dosage', 'precautions', 
        ]
    ordering = ['name']
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
    def clean_decimal_value(value, row_num=None, cell_type=None):
        """숫자 데이터를 정제하고 Decimal로 변환하는 함수"""
        # print(f"행 {row_num} 처리 시작")
        # print(f"- 원본 값: '{value}'")
        # print(f"- 셀 타입: {cell_type}")
        
        try:
            # xlrd의 셀 타입이 숫자인 경우 (XL_CELL_NUMBER = 2)
            if cell_type == xlrd.XL_CELL_NUMBER:
                # 부동소수점 오차를 줄이기 위해 문자열로 변환 후 처리
                str_value = f"{float(value):.4f}"
                return Decimal(str_value)
            
            # 숫자인 경우 처리
            if isinstance(value, (int, float)):
                return Decimal(f"{float(value):.4f}")
            
            # 문자열인 경우 처리
            if isinstance(value, str):
                cleaned = value.strip().replace(",", "")
                if not cleaned or any(c.isalpha() for c in cleaned):
                    return Decimal('0')
                return Decimal(f"{float(cleaned):.4f}")
            
            # 기본 처리
            return Decimal('0')
            
        except (InvalidOperation, ValueError, TypeError) as e:
            print(f"- 변환 실패: {str(e)}")
            return Decimal('0')

    for obj in queryset:
        if not obj.file:
            modeladmin.message_user(request, f"'{obj}'에 대한 파일이 없습니다.", level=messages.WARNING)
            continue

        try:
            workbook = xlrd.open_workbook(file_contents=obj.file.read())
            sheet = workbook.sheet_by_index(0)
            
            success_count = 0
            error_count = 0
            new_items = 0
            
            header_row = sheet.row_values(0)

            # 재고량 컬럼 인덱스 찾기
            try:
                quantity_col = header_row.index('재고량')
            except ValueError:
                modeladmin.message_user(request, "재고량 컬럼을 찾을 수 없습니다.", level=messages.ERROR)
                continue
            
            # 상한가 컬럼 인덱스 찾기
            try:
                price_col = header_row.index('상한가')
            except ValueError:
                modeladmin.message_user(request, "상한가 컬럼을 찾을 수 없습니다.", level=messages.ERROR)
                continue

            for row in range(1, sheet.nrows):  # 헤더 제외
                try:
                    row_values = sheet.row_values(row)
                    cell_type = sheet.cell_type(row, quantity_col)  # 셀 타입 확인
                    cell_type_price = sheet.cell_type(row, price_col)  # 상한가 셀 타입 확인
                    
                    product_name = str(row_values[0]).strip()
                    if not product_name or product_name == '약품명':
                        continue

                    product_company = str(row_values[3]).strip()
                    product_quantity = clean_decimal_value(row_values[quantity_col], row + 1, cell_type)
                    if product_quantity < Decimal('0'):
                        product_quantity = Decimal('0')
                    
                    product_code = str(row_values[1]).strip()
                    product_price = clean_decimal_value(row_values[4], row + 1, cell_type_price)
                    if product_price < Decimal('0'):
                        product_price = Decimal('0')

                    # print(f"\n처리 결과:")
                    # print(f"제품명: {product_name}")
                    # print(f"재고량: {product_quantity}")
                    # print(f"저장 준비 - 제품명: {product_name}, 회사명: {product_company}, 재고량: {product_quantity}")

                    etcs = Etc.objects.filter(name__contains=product_name)
                    
                    if etcs.exists():
                        for etc in etcs:
                            if len(etc.name) == len(product_name):
                                etc.quantity = product_quantity
                                etc.order = etc.target - product_quantity
                                etc.code = product_code
                                etc.price = product_price
                                etc.save()
                                success_count += 1
                    else:
                        product_target = Decimal('0')
                        product_order = product_target - product_quantity
                        if product_order < Decimal('0'):
                            product_order = Decimal('0')
                        new_object = Etc(
                            name=product_name,
                            company=product_company,
                            quantity=product_quantity,
                            target=product_target,
                            order=product_order,
                            code=product_code,
                            price=product_price
                        )
                        new_object.save()
                        new_items += 1

                except Exception as e:
                    error_count += 1
                    print(f"행 {row + 1} 처리 중 오류 발생: {str(e)}")
                    import traceback
                    print(traceback.format_exc())  # 상세한 오류 추적
                    continue

            # 결과 메시지 생성
            message_parts = []
            if success_count > 0:
                message_parts.append(f"{success_count}개 항목 업데이트 성공")
            if new_items > 0:
                message_parts.append(f"{new_items}개 새로운 항목 추가")
            if error_count > 0:
                message_parts.append(f"{error_count}개 항목 처리 실패")

            result_message = ", ".join(message_parts)
            level = messages.SUCCESS if error_count == 0 else messages.WARNING
            modeladmin.message_user(request, f"재고 최신화 완료: {result_message}", level=level)

        except Exception as e:
            modeladmin.message_user(
                request, 
                f"파일 '{obj.file.name}' 처리 중 오류 발생: {str(e)}", 
                level=messages.ERROR
            )            

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
    
    def delete_queryset(self, request, queryset):
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


@admin.action(description="유효기간 입력하기")
def process_files(modeladmin, request, queryset):
    for obj in queryset:
        if obj.file:
            try:
                workbook = xlrd.open_workbook(file_contents=obj.file.read())
                sheet = workbook.sheet_by_index(0)

                for row in range(sheet.nrows):
                    if sheet.row_values(row)[0] != '약품명':
                        product_name = sheet.row_values(row)[0]
                        product_expiry = sheet.row_values(row)[8]
                        product_order = sheet.row_values(row)[3]
                        
                        etcs = Etc.objects.filter(name__contains=product_name)
                        if etcs.exists():
                            for etc in etcs:
                                if etc.name == product_name and etc.quantity > 0:
                                    if product_expiry:
                                        if etc.expiry:
                                            if etc.expiry < int(product_expiry):
                                                etc.old_expiry = etc.expiry
                                                etc.expiry = int(product_expiry)
                                        else:
                                            etc.expiry = int(product_expiry)
                                etc.last = product_order
                                etc.save()
                        else:
                            modeladmin.message_user(
                                request,
                                f"{product_name}은 아직 등록되지 않은 제품입니다.",
                                level='WARNING'
                            )
                
                modeladmin.message_user(request, "파일 처리가 완료되었습니다.")
            except Exception as e:
                modeladmin.message_user(request, f"오류 발생: {str(e)}", level='ERROR')


@admin.register(RespiryRegist)
class RespiryRegistAdmin(admin.ModelAdmin):
    form = RespiryRegistForm
    list_display = ('file', 'uploaded_at')
    actions = [process_files]  # 여기서 함수 이름만 문자열로 참조
    
    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('file')
        if files:  # 파일이 선택된 경우에만 처리
            for f in files:
                # 각 파일에 대해 새로운 ProductRegist 인스턴스 생성
                instance = RespiryRegist(file=f)
                instance.save()
        else:  # 파일이 없는 경우 기본 저장 동작 수행
            super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if obj.file:
            obj.file.delete(save=False)
        obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                if obj.file:
                    file_path = obj.file.path
                    obj.file.close()
                    obj.file.delete(save=False)
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except PermissionError:
                continue
        queryset.delete()