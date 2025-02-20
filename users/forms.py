from django import forms
from users.models import User

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label="아이디")
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="비밀번호")
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8, label="비밀번호 확인")
    name = forms.CharField(max_length=30, required=False, label="이름")
    email = forms.EmailField(max_length=50, required=False, label="이메일")
    phone_number = forms.CharField(max_length=30, required=False, label="휴대폰번호")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 존재하는 아이디입니다.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data