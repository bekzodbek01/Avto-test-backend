from rest_framework import serializers
from .models import Marathon, Option, OptionAnswer, Category


class OptionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionAnswer
        fields = ['user', 'option', 'text', 'is_correct']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class MarathonSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Marathon
        fields = ['id', 'title', 'text', 'image', 'created_at', 'options']


class CategorySerializer(serializers.ModelSerializer):
    marathons = MarathonSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'marathons']