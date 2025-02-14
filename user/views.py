from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .vaildators import vaildate_user_data
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated



class UserCreateView(APIView):
    def post(self, request):
        # 유효성 검사하기
        rlt_message = vaildate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=400)
        
        vaildated_data = {
            "username": request.data.get("username"), # 아이디
            "nickname": request.data.get("nickname"),
            "password": request.data.get("password"),
        }

        user = User.objects.create_user(**vaildated_data)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)
    

class UserSigninView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"message": "아이디 또는 비밀번호가 다릅니다."}, status=400
            )
        refresh = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_info": serializer.data,
            }
        )
    

class UserSignoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"message": "로그아웃이 되지 않았습니다."}, status=400)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "로그아웃이 완료되었습니다."}, status=205)