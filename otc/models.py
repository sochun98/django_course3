from django.db import models


class Otc(models.Model):
    # 제품명
    name = models.CharField(max_length=50)
    # 제조업체
    company = models.CharField(max_length=50)
    # 약품코드
    code = models.CharField(max_length=25)
    # 재고량
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    # 적정재고량
    target = models.DecimalField(max_digits=5, decimal_places=2)
    # 적정재고량 - 재고량 = 주문량
    order = models.DecimalField(max_digits=5, decimal_places=2)


class ExcelUpload(models.Model):
    file = models.FileField(upload_to='excel_files/')
