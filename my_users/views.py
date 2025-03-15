from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            return Response({'message': "Telefon raqami allaqachon ro'yxatdan o'tgan!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=True)

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        name = serializer.validated_data['name']

        try:
            user = CustomUser.objects.get(phone=phone)

            # Foydalanuvchi nomini tekshirish
            if user.name != name:
                return Response({'message': 'Foydalanuvchi nomi yoki telefon raqami noto\'g\'ri!'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Admin tomonidan tasdiqlanmagan bo'lsa, foydalanuvchi tizimga kira olmaydi
            if not user.is_active:
                return Response({'message': 'Admin ruxsat berishini kuting!'},
                                status=status.HTTP_400_BAD_REQUEST)

            # JWT tokenlarini yaratish
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'message': 'Ro\'yxatdan o\'tmagan foydalanuvchi. Iltimos, ro\'yxatdan o\'ting.'},
                            status=status.HTTP_400_BAD_REQUEST)
