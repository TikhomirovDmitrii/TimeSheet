from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Регистрация пользователя"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Заполните все поля'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь уже существует'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'Пользователь создан'}, status=201)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Авторизация пользователя и выдача JWT-токена"""
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    return Response({"error": "Неверные учетные данные"}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Получение информации о текущем пользователе"""
    return Response({'username': request.user.username})
