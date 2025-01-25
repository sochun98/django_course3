from django.db import models
from django.forms import ValidationError
from ingredient.models import Ingredient


class Etc(models.Model):
    # 약품명(0)
    name = models.CharField(max_length=50)
    # 약품코드(1)
    code = models.CharField(max_length=20)
    # 성분명(2)
    ingredients = models.ManyToManyField(Ingredient, related_name='etc_products', blank=True)
    # 제조업체(3)
    company = models.CharField(max_length=50)
    # 상한가(4)
    price = models.IntegerField(null=True, blank=True)
    # 재고량(7)
    quantity = models.DecimalField(max_digits=6, decimal_places=4, default=False)
    # 적정재고량
    quantity = models.DecimalField(max_digits=6, decimal_places=4, default=False)
    # 주문량 = 적정재고량 - 재고량
    quantity = models.DecimalField(max_digits=6, decimal_places=4, default=False, null=True, blank=True)
    # 유효기간
    expiry = models.IntegerField(null=True, blank=True)
    # 이전 유효기간
    old_expiry = models.IntegerField(null=True, blank=True)
    # 효능
    effects = models.TextField(null=True, blank=True)
    # 용법
    dosage = models.TextField(null=True, blank=True)
    # 주의사항
    precautions = models.TextField(null=True, blank=True)


class EtcUpload(models.Model):
    file = models.FileField(upload_to='etc_files/')
    
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


class OrderList(models.Model):
    # 주문일자
    datetime = models.DateTimeField(auto_now_add=True)
    # 제조업체
    company = models.CharField(max_length=50)
    # 주문내역
    content = models.TextField(blank=True, null=True)


class RespiryRegist(models.Model):
    file = models.FileField(upload_to='etc_respiryregist_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        try:
            return str(self.file.name)
        except AttributeError:
            return "Multiple files"
    
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    def clean(self):
        if hasattr(self.file, 'name'):
            file_extension = self.file.name.split('.')[-1].lower()
            if file_extension != 'xls':
                raise ValidationError('올바른 파일 형식이 아닙니다. xls 파일만 업로드 가능합니다.')