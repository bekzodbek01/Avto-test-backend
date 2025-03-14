from rest_framework import serializers
from .models import CustomUser

# Register serializer: Foydalanuvchi ro'yxatdan o'tishda faqat phone, name, va last_name talab qilinadi
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone', 'name', 'last_name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone=validated_data['phone'],
            name=validated_data['name'],
            last_name=validated_data['last_name']
        )
        return user

# Login serializer: Foydalanuvchi tizimga kirishda faqat phone va name kiritadi
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=50)
