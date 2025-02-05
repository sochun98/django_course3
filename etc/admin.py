from decimal import Decimal, InvalidOperation
import decimal
import os
from django.contrib import admin, messages
import xlrd
from etc.actions import etc_update, process_files, product_order
from etc.forms import EtcUploadForm, RespiryRegistForm
from etc.models import Etc, EtcUpload, OrderList, RespiryRegist
        

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