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


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


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

#
# class TicketSerializer(serializers.ModelSerializer):
#     marathon = MarathonSerializer()
#     questions = OptionSerializer(many=True)
#
#     class Meta:
#         model = Ticket
#         fields = ['id', 'marathon', 'questions']
#
#
# class UserTicketSerializer(serializers.ModelSerializer):
#     """Foydalanuvchiga ajratilgan biletlar serializeri"""
#     ticket = TicketSerializer(read_only=True)
#
#     class Meta:
#         model = UserTicket
#         fields = ['id', 'user', 'ticket', 'created_at']
#
#
# class UserTicketResultSerializer(serializers.ModelSerializer):
#     """Foydalanuvchi bilet natijalari uchun serializer"""
#     ticket = TicketSerializer(source="user_ticket.ticket", read_only=True)
#     selected_options = OptionSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = UserTicketResult
#         fields = [
#             'id', 'user_ticket', 'ticket', 'total_correct_answers',
#             'total_incorrect_answers', 'correct_percentage', 'selected_options'
#         ]
