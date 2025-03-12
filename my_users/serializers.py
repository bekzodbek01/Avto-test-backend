from rest_framework import serializers
from .models import CustomUser, GlobalUserInfo
from rest_framework.validators import UniqueValidator


class GlobalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalUserInfo
        fields = ('card_number', 'telegram_username', 'message')


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'last_name')
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, data):
        phone = data.get('phone')
        name = data.get('name')

        if phone and name:
            try:
                user = CustomUser.objects.get(phone=phone, name=name)
                if not user.is_active:
                    global_info = GlobalUserInfo.objects.first()
                    raise serializers.ValidationError({
                        'card_number': global_info.card_number,
                        'telegram_username': global_info.telegram_username,
                        'message': global_info.message,
                        'detail': 'Please make a payment and contact the admin to activate your account.'
                    })
                data['user'] = user
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Please register before logging in.")
        else:
            raise serializers.ValidationError("Must include 'phone' and 'name'.")

        return data
