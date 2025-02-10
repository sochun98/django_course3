from django.db import models
from django.core.exceptions import ValidationError
from ingredient.models import Ingredient

class Otc(models.Model):
    # 제품명
    name = models.CharField(max_length=50)
    # 제조업체
    company = models.CharField(max_length=50)
    # 재고량
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=False)
    # 적정재고량
    target = models.DecimalField(max_digits=5, decimal_places=2, default=False)
    # 적정재고량 - 재고량 = 주문량
    order = models.DecimalField(max_digits=5, decimal_places=2, default=False, null=True, blank=True)
    # 유효기간
    expiry = models.IntegerField(null=True, blank=True)
    # 이전 유효기간
    old_expiry = models.IntegerField(null=True, blank=True)
    # 마지막 주문량
    last = models.DecimalField(max_digits=5, decimal_places=2, default=False, null=True, blank=True)
    # 성분
    ingredients = models.ManyToManyField(Ingredient, related_name='otc_products',  blank=True)
    # 효능
    effects = models.TextField(null=True, blank=True)
    # 용법
    dosage = models.TextField(null=True, blank=True)
    # 주의사항
    precautions = models.TextField(null=True, blank=True)


class OtcUpload(models.Model):
    file = models.FileField(upload_to='files/otc_files/')
    
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
    file = models.FileField(upload_to='otc_respiryregist_files/')
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
        if hasattr(self.file, 'name'):  # 단일 파일인 경우
            file_extension = self.file.name.split('.')[-1].lower()
            if file_extension != 'xls':
                raise ValidationError('올바른 파일 형식이 아닙니다. xls 파일만 업로드 가능합니다.')
        """elif isinstance(self.file, list):  # 다중 파일인 경우
            for f in self.file:
                if hasattr(f, 'name'):
                    file_extension = f.name.split('.')[-1].lower()
                    if file_extension != 'xls':
                        raise ValidationError(f'{f.name}는 올바른 파일 형식이 아닙니다. xls 파일만 업로드 가능합니다.')"""


