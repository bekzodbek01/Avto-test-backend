from rest_framework import serializers
from .models import Category, Marathon, Option, UserAnswer


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'extra_info', 'is_correct']


class MarathonSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Marathon
        fields = ['id', 'title', 'text', 'image', 'options']


class CategorySerializer(serializers.ModelSerializer):
    marathons = MarathonSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'marathons']


class UserAnswerSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all(), many=True)

    class Meta:
        model = UserAnswer
        fields = ['user', 'selected_options', 'is_correct', 'created_at']
