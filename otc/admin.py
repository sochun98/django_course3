import decimal
from django.contrib import admin
from otc.models import Otc
from otc.models import ExcelUpload
from otc.forms import ExcelUploadForm
from openpyxl import load_workbook
from django.conf import settings
from decimal import Decimal


@admin.register(Otc)
class OtcAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'company', 'quantity', 'target', 'order',
    ]
    fields = ['name', 'company', 'target',]
    list_filter = ['order', ]
    search_fields = ['name', 'company', ]


@admin.action(description="판매약품 재고 최신화")
def otc_update(modeladmin, request, queryset):
    
    if queryset and isinstance(queryset.first(), ExcelUpload):
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
                for otc in otcs:
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
            
        
        


@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    form = ExcelUploadForm
    actions = [otc_update]
