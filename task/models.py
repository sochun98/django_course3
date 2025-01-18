from django.db import models


class Return(models.Model):
    # 반품요청일자(Entry Date)
    entry = models.IntegerField()
    # 회수일자(Recall Date)
    recall = models.IntegerField(null=True, blank=True)
    # 완료일자(Completion Date)
    completion = models.IntegerField(null=True, blank=True)
    # 제품명
    name = models.CharField(max_length=50)
    # 약품코드
    code = models.IntegerField(null=True, blank=True)
    # 규격(정/병) (Specification)
    spec = models.IntegerField(null=True, blank=True)
    # 제조번호 (Lot Number)
    lot = models.IntegerField(null=True, blank=True)
    # 유효기간 (Expiry)
    expiry = models.IntegerField(null=True, blank=True)
    # 개수(병) (Spec Number)
    spec_num = models.IntegerField(null=True, blank=True)
    # 개수(낱개) (Unit Number)
    unit_num = models.DecimalField(max_digits=5, decimal_places=1, default=False, null=True, blank=True)
    # 단위가격 (Unit Price)
    unit_price = models.IntegerField(null=True, blank=True)
    # 전체개수 (Total Quantity)
    total_quantitiy = models.DecimalField(max_digits=7, decimal_places=1, default=False, null=True, blank=True)
    # 전체가격 (Total Price)
    total_price = models.DecimalField(max_digits=15, decimal_places=1, default=False, null=True, blank=True)
    # 합산가격 (Cummulative Price)
    # cum_price = models.DecimalField(max_digits=17, decimal_places=1, default=False, null=True, blank=True)