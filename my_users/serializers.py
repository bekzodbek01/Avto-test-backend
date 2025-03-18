from rest_framework import serializers
from .models import CustomUser, GlobalUserInfo


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone', 'name', 'last_name']

    def create(self, validated_data):
        # Foydalanuvchini yaratish
        user = CustomUser.objects.create_user(
            phone=validated_data['phone'],
            name=validated_data['name'],
            last_name=validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=50)


class GlobalUserInfSerializers(serializers.ModelSerializer):
    class Meta:
        model = GlobalUserInfo
        fields = ['id', 'card_number', 'telegram_username', 'message']

