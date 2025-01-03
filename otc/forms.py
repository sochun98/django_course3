from django import forms
from otc.models import ExcelUpload


class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelUpload
        fields = ('file',)
