import decimal
# import os
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
import xlrd
from otc.models import Otc, OtcUpload, OrderList, ProductRegist
from otc.forms import OtcUploadForm, ProductRegistForm
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.conf import settings
from decimal import Decimal
# import pandas as pd


@admin.action(description="제품 주문서 작성하기")
def product_order(modeladmin, request, queryset):
    data = []
    for row in queryset:
        processed_row = row.name + ' : ' + str(int(row.order)) + ' EA'
        data.append(processed_row)
        company = row.company
    
    combined_data = ", \n".join(data)
        
    content = '안녕하세요 더샵참약국입니다.\n' + combined_data + '\n주문할게요 감사합니다!'
    
    new_object = OrderList(company=company, content=content)
    new_object.save()
    print("주문서 작성이 완료되었습니다.")


@admin.register(Otc)
class OtcAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'company', 'quantity', 'target', 'order', 'expiry', 'last', 'get_ingredients',
    ]
    fields = ['name', 'company', 'target', 'order', 'expiry', 'ingredients', 'effects', 'dosage', 'precautions', ]
    filter_horizontal = ['ingredients'] # 다대다 관계를 위한 편리한 인터페이스
    list_filter = ['order', ]
    search_fields = ['name', 'company', 'ingredients__name', 'effects',]
    actions = [product_order]
    
    def get_ingredients(self, obj):
        return ", ".join([i.name for i in obj.ingredients.all()])
    get_ingredients.short_description = '성분'


@admin.action(description="판매약품 재고 최신화")
# xls 확장자
def otc_update(modeladmin, request, queryset):
    for obj in queryset:
        if obj.file:
            try:
                workbook = xlrd.open_workbook(file_contents=obj.file.read())
                sheet = workbook.sheet_by_index(0)
                
                for row in range(sheet.nrows):
                    if sheet.row_values(row)[1] != '제조업체':
                        product_name = sheet.row_values(row)[0]
                        product_company = sheet.row_values(row)[1]
                        
                        try:
                            decimal_number = Decimal(sheet.row_values(row)[3])
                        except decimal.InvalidOperation:
                            print("잘못된 숫자 형식입니다.")
                        product_quantity = decimal_number
                        
                        otcs = Otc.objects.filter(name__contains=product_name)
                        
                        if otcs.exists():
                            for otc in otcs:
                                if len(otc.name) == len(product_name):
                                    otc.quantity = product_quantity
                                    otc.order = otc.target - product_quantity
                                    otc.save()
                        else:
                            product_target = 0
                            product_order = product_target - product_quantity
                            new_object = Otc(name=product_name, company=product_company, quantity=product_quantity, target=product_target, order=product_order)
                            new_object.save()
                            print("새로운 품목이 추가되었습니다.")
    
                print("재고 최신화가 완료되었습니다.")

                modeladmin.message_user(request, "판매약품 재고 최신화 되었습니다.")
            except Exception as e:
                modeladmin.message_user(request, f"Error reading file '{obj.file.name}': {str(e)}", level='error')
        else:
            modeladmin.message_user(request, f"No file uploaded for '{obj}'.", level='warning')
    
# xlsx 확장자
"""
def otc_update(modeladmin, request, queryset):
    
    if queryset and isinstance(queryset.first(), OtcUpload):
        for upload in queryset:
            if hasattr(upload, 'file'):
                # file이 FileField인 경우
                file_name = upload.file.name
            elif hasattr(upload, 'file_name'):
                # file_name이 CharField인 경우
                file_name = upload.file_name
            else:
                print("파일 이름을 찾을 수 없습니다.")
                continue

            print(f"업로드된 파일 이름: {file_name}")
            # 여기서 file_name을 사용하여 파일을 읽는 등의 작업을 할 수 있습니다.
    
    # 이후의 코드 (파일 읽기 등)는 file_name을 사용하여 수정
    # file_path = settings.BASE_DIR / "excel_files" / file_name
    file_path = settings.BASE_DIR / file_name
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    
    data = []
    for row in sheet.iter_rows(values_only=True):
        processed_row = [str(cell).strip() if cell else '' for cell in row]
        data.append(processed_row)
    
    
    for row in data:
        if row[1] != '제조업체':
            product_name = row[0]
            product_company = row[1]
            
            try:
                decimal_number = Decimal(row[3])
            except decimal.InvalidOperation:
                print("잘못된 숫자 형식입니다.")
            product_quantity = decimal_number
            
            otcs = Otc.objects.filter(name__contains=product_name)
            
            if otcs.exists():
                # if len(otcs) > 1:
                    # print(len(otcs))
                    # print(product_name)
                    # print('----------')
                for otc in otcs:
                    if len(otc.name) == len(product_name):
                        otc.quantity = product_quantity
                        otc.order = otc.target - product_quantity
                        otc.save()
                # print("수정 완료되었습니다.")
            else:
                product_target = 0
                product_order = product_target - product_quantity
                new_object = Otc(name=product_name, company=product_company, quantity=product_quantity, target=product_target, order=product_order)
                new_object.save()
                print("새로운 품목이 추가되었습니다.")
    
    print("재고 최신화가 완료되었습니다.")
"""
            
"""

@admin.action(description="파일포맷변환_xls_to_xlsx")
def file_convert(modeladmin, request, queryset):
    if queryset and isinstance(queryset.first(), OtcUpload):
        for upload in queryset:
            if hasattr(upload, 'file'):
                 # FileField에서 파일의 실제 경로를 얻습니다
                file_path = upload.file.path
                # file_path = upload.file.path.replace('\\', '/')
            else:
                print("파일 이름을 찾을 수 없습니다.")
                continue

            print(f"업로드된 파일 이름: {file_path}")

    # 파일의 기본 이름과 디렉토리를 얻습니다
    base_name = os.path.splitext(file_path)[0]
    directory = os.path.dirname(file_path)
    
    # 새로운 파일 이름을 만듭니다
    new_file_name = f"{base_name}.xlsx"
    output_file = os.path.join(directory, new_file_name)
    
    # 파일 이름을 변경합니다
    # os.rename(file_path, output_file)
    print(f"파일이 성공적으로 '{output_file}'로 변경되었습니다.")
    
    # 변환 작업

    try:
        # .xls 파일을 읽습니다
        wb = xlrd.open_workbook(file_path)
        sh = wb.sheet_by_index(0)
                
        # 데이터를 pandas DataFrame으로 변환
        data = []
        for rownum in range(sh.nrows):
            data.append(sh.row_values(rownum))
        df = pd.DataFrame(data[1:], columns=data[0])  # 첫 번째 행을 헤더로 사용

        # 새로운 .xlsx 파일을 생성합니다 (여기서는 .xlsl로 저장하지만, 실제로는 .xlsx가 맞을 수 있음)
        wb_xlsx = Workbook()
        ws = wb_xlsx.active

        # DataFrame을 .xlsl 파일로 변환
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

        # 파일 저장
        wb_xlsx.save(output_file)
        modeladmin.message_user(request, f"File '{file_path}' converted to '{output_file}' successfully.", level='info')
    except Exception as e:
        modeladmin.message_user(request, f"Error converting file '{file_path}': {str(e)}", level='error')
"""
        
@admin.register(OtcUpload)
class OtcUploadAdmin(admin.ModelAdmin):
    form = OtcUploadForm
    actions = [otc_update]
    list_display = ('get_file_name',)
    
    def get_file_name(self, obj):
        return obj.file.name
    get_file_name.short_description = '파일 이름'
    
    def delete_model(self, request, obj):
        # 파일 삭제
        if obj.file:
            obj.file.delete(save=False)
        # 모델 인스턴스 삭제
        obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
        queryset.delete()


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'datetime', 'company', 
    ]
    fields = ['company', 'content', ]
    # list_filter = []
    search_fields = ['datetime', 'company', 'content', ]

"""
@admin.action(description="의약품 유효기간 입력")
def product_regist(modeladmin, request, queryset):
    for obj in queryset:
        if obj.file:
            try:
                workbook = xlrd.open_workbook(file_contents=obj.file.read())
                sheet = workbook.sheet_by_index(0)

                for row in range(sheet.nrows):
                    if sheet.row_values(row)[0] != '약품명':
                        product_name = sheet.row_values(row)[0]
                        product_expiry = sheet.row_values(row)[8]
                        print(f"제품명 : {product_name}, 유효기간 : {product_expiry}")
                        
                        otcs = Otc.objects.filter(name__contains=product_name)
                        
                        if otcs.exists():
                            for otc in otcs:
                                if len(otc.name) == len(product_name) and otc.quantity > 0:
                                    otc.expiry = product_expiry
                                    otc.save()
                        else:
                            modeladmin.message_user(request, f"{product_name}은 아직 등록되지 않은 제품입니다. otc update를 통해서 등록한 후에 유효기간을 입력하시기 바랍니다.")
                            

                modeladmin.message_user(request, f"Excel file '{obj.file.name}' has been read successfully.")
            except Exception as e:
                modeladmin.message_user(request, f"Error reading file '{obj.file.name}': {str(e)}", level='error')
        else:
            modeladmin.message_user(request, f"No file uploaded for '{obj}'.", level='warning')
"""


@admin.register(ProductRegist)
class ProductRegistAdmin(admin.ModelAdmin):
    form = ProductRegistForm
    list_display = ('file', 'uploaded_at')
    
    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('file')
        if files:  # 파일이 선택된 경우에만 처리
            for f in files:
                # 각 파일에 대해 새로운 ProductRegist 인스턴스 생성
                instance = ProductRegist(file=f)
                instance.save()
        else:  # 파일이 없는 경우 기본 저장 동작 수행
            super().save_model(request, obj, form, change)
            
    def process_files(self, request, queryset):
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
                            
                            otcs = Otc.objects.filter(name__contains=product_name)
                            if otcs.exists():
                                for otc in otcs:
                                    if otc.name == product_name and otc.quantity > 0:
                                        if product_expiry:
                                            otc.expiry = int(product_expiry)
                                        # 유효기간이 큰 값으로 저장
                                        """
                                        otc.last = product_order
                                        if otc.expiry.exists():
                                            if otc.expiry < product_expiry:
                                                otc.expiry = product_expiry
                                        else:
                                            otc.expiry = product_expiry
                                        """
                                        otc.save()
                            else:
                                self.message_user(
                                    request,
                                    f"{product_name}은 아직 등록되지 않은 제품입니다.",
                                    level='WARNING'
                                )
                    
                    self.message_user(request, "파일 처리가 완료되었습니다.")
                except Exception as e:
                    self.message_user(request, f"오류 발생: {str(e)}", level='ERROR')
    
    process_files.short_description = "유효기간 입력하기"
    actions = ['process_files']
    
    def delete_model(self, request, obj):
        if obj.file:
            obj.file.delete(save=False)
        obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file:
                obj.file.delete(save=False)
        queryset.delete()
