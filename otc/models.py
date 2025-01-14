from django.db import models
from django.core.exceptions import ValidationError


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
    expiry = models.CharField(max_length=8, null=True, blank=True)


class OtcUpload(models.Model):
    file = models.FileField(upload_to='otc_files/')
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
    

class OrderList(models.Model):
    # 주문일자
    datetime = models.DateTimeField(auto_now_add=True)
    # 제조업체
    company = models.CharField(max_length=50)
    # 주문내역
    content = models.TextField(blank=True, null=True)
    

class ProductRegist(models.Model):
    file = models.FileField(upload_to='productregist_files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name
    
    def clean(self):
        file_extension = self.file.name.split('.')[-1].lower()
        if file_extension != 'xls':
            raise ValidationError('올바른 파일 형식이 아닙니다. xls 파일만 업로드 가능합니다.')


