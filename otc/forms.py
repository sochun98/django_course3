from django import forms
from otc.models import OtcUpload, ProductRegist


class OtcUploadForm(forms.ModelForm):
    class Meta:
        model = OtcUpload
        fields = ('file',)


class ProductRegistForm(forms.ModelForm):
    class Meta:
        model = ProductRegist
        fields = ['file',]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }