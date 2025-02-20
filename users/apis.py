from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from users.serializers import SignupSerializer, LoginSerializer
from users.models import User, Jwt
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from users.utils import get_access_token, get_refresh_token
from django.shortcuts import render, redirect
from django.urls import reverse


class SignupAPI(APIView):
    serializer_class = SignupSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("password2")
        user = User.objects.create_user(
            **serializer.validated_data
        )
        return Response(status=status.HTTP_201_CREATED, data={"message":f"{user.username}님 회원가입이 완료되었습니다."})


class LoginAPI(APIView):
    serializer_class = LoginSerializer
    
    def get(self, request):
        # GET 요청 시 로그인 템플릿 렌더링
        return render(request, 'registration/login.html')

    
    def post(self, request):
        # POST 요청 시 API 인증 로직 처리
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password"),
        )
        if user is None:
            return render(request, "registration/login.html", {'error':'아이디 또는 비밀번호가 올바르지 않습니다.'})
        
        # jwt 토큰 삭제
        Jwt.objects.filter(user=user).delete()
        
        # jwt 토큰 발급
        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()
        
        Jwt.objects.create(
            user=user,
            access=access,
            refresh=refresh
        )
        
        # Django 세션 로그인
        login(request, user)
        
        # API 응답 생성
        """
        response = Response(status=status.HTTP_200_OK)
        data = {
            "access": access,
        }
        response.data = data
        response.set_cookie(key="access", value=access)
        response.set_cookie(key="refresh", value=refresh, httponly=True)
        """
         # 리다이렉션 응답 생성
        redirect_response = HttpResponseRedirect(reverse('todo_list'))

        # 쿠키 설정
        redirect_response.set_cookie(key="access", value=access)
        redirect_response.set_cookie(key="refresh", value=refresh, httponly=True)

        return redirect_response
        


class LogoutAPI(APIView):
    
    def get(self, request):
        
        # jwt 토큰 삭제
        from users.utils import decodeJWT
        user = decodeJWT(request.META.get("HTTP_AUTHORIZATION"))
        if user != "expired" and user != "decode_error" and user is not None:
            Jwt.objects.filter(user=user).delete()
        
        # 세션 로그아웃
        logout(request)
        
        # 쿠키 삭제
        response = redirect("/login/")
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        
        return response