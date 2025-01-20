from django.db import models


class Return(models.Model):
    # 반품요청일자(Entry Date)
    entry = models.IntegerField()
    # 회수일자(Recall Date)
    recall = models.IntegerField(null=True, blank=True)
    # 완료일자(Completion Date)
    completion = models.IntegerField(null=True, blank=True)
    # 제조회사
    company = models.CharField(max_length=50)
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
    unit_num = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True, blank=True)
    # 단위가격 (Unit Price)
    unit_price = models.IntegerField(null=True, blank=True)
    # 전체개수 (Total Quantity)
    total_quantity = models.DecimalField(max_digits=7, decimal_places=1, default=0, null=True, blank=True)
    # 전체가격 (Total Price)
    total_price = models.DecimalField(max_digits=15, decimal_places=1, default=0, null=True, blank=True)
    # 합산가격 (Cummulative Price)
    cum_price = models.DecimalField(max_digits=17, decimal_places=1, default=0, null=True, blank=True)
    
    
class ReturnList(models.Model):
    # 반품요청일자
    datetime = models.DateTimeField(auto_now_add=True)
    # 제조회사, 거래처
    company = models.CharField(max_length=50)
    # 반품내역
    content = models.TextField(blank=True, null=True)


class Set(models.Model):
    # 세트명
    name = models.CharField(max_length=50)
    # 구성품
    comp1 = models.CharField(max_length=50, null=True, blank=True)
    comp2 = models.CharField(max_length=50, null=True, blank=True)
    comp3 = models.CharField(max_length=50, null=True, blank=True)
    # 구성품 가격
    price1 = models.IntegerField(default=0)
    price2 = models.IntegerField(default=0)
    price3 = models.IntegerField(default=0)
    price_sum = models.IntegerField(default=0)
    # 판매가격
    price_sell = models.IntegerField(default=0)
    # 제품 바코드
    code = models.IntegerField(null=True, blank=True)
    # 제품 설명
    content = models.TextField(null=True, blank=True)
    

class Profit(models.Model):
    # 날짜
    date = models.IntegerField()
    # 현금입금
    bill_10k = models.IntegerField(default=0)
    bill_5k = models.IntegerField(default=0)
    bill_1k = models.IntegerField(default=0)
    # 약품판매약
    otc_in = models.IntegerField()
    # 판매할인액
    otc_discount = models.IntegerField()
    # 판매마진액
    otc_margin = models.IntegerField()
    # 처방, 판매 건수
    presc_num = models.IntegerField()
    otc_num = models.IntegerField()
    # 조제 입금
    presc_in = models.IntegerField()
    presc_bill = models.IntegerField()
    presc_card = models.IntegerField()
    # 약품판매(현금, 카드)
    otc_bill = models.IntegerField()
    otc_card = models.IntegerField()
    # 처방조제약품 가격
    medicine_insur = models.IntegerField()
    medicine_nonsur = models.IntegerField()
    # 조제료 (presc_sum = presc_insur + presc_nonsur)
    presc_insur = models.IntegerField()
    presc_nonsur = models.IntegerField()
    presc_sum = models.IntegerField(default=0)
    # 카드입금
    card_in = models.IntegerField()
    # 조제판매마진 (presc_sum + otc_margin)
    margin_sum = models.IntegerField(default=0)
    # 계산을 통해서 검증 가능
    # presc_calc = 10000*bill_10k + 5000*bill_5k + 1000*bill_1k + presc_card + otc_card + otc_discount + amount_billing - (otc_in + medicine_insur + medicine_nonsur)
    presc_calc = models.IntegerField(default=0)
    # otc_calc = otc_card + otc_bill + otc_discount
    otc_calc = models.IntegerField(default=0)
    # bill_calc = presc_in + otc_in - (presc_card + otc_card + otc_discount)
    bill_calc = models.IntegerField(default=0)
    # card_calc = presc_card + otc_card
    card_calc = models.IntegerField(default=0)
    