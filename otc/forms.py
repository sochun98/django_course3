from django import forms
from otc.models import OtcUpload


class OtcUploadForm(forms.ModelForm):
    class Meta:
        model = OtcUpload
        fields = ('file',)
