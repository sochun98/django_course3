from django.views import View
from django.shortcuts import render, redirect
from users.forms import SignupForm
from users.models import User

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # 사용자 생성
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number']
            )
            return redirect('login')  # 회원가입 후 로그인 페이지로 이동
        return render(request, 'registration/signup.html', {'form': form})
