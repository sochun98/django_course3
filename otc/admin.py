import decimal
import os
# import os
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
import xlrd
from otc.models import Otc, OtcUpload, OrderList, RespiryRegist
from otc.forms import OtcUploadForm, RespiryRegistForm
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.conf import settings
from decimal import Decimal
from otc.actions import process_files, product_order, otc_update
# import pandas as pd


@admin.register(Otc)
class OtcAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'company', 'quantity', 'target', 'order', 'expiry', 'last', 'get_ingredients',
    ]
    fields = ['company', 'name', 'target', 'order', 'expiry', 'old_expiry', 'ingredients', 'effects', 'dosage', 'precautions', ]
    filter_horizontal = ['ingredients'] # 다대다 관계를 위한 편리한 인터페이스
    list_filter = ['order', ]
    search_fields = ['name', 'company', 'ingredients__name', 'effects',]
    actions = [product_order]
    
    def get_ingredients(self, obj):
        return ", ".join([i.name for i in obj.ingredients.all()])
    get_ingredients.short_description = '성분'

        
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