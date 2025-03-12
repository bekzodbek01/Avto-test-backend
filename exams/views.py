from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Marathon, Option, OptionAnswer, Category
from .serializers import OptionAnswerSerializer, MarathonSerializer, CategorySerializer
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import OptionAnswerSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class OptionAnswerCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OptionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            # Javobni saqlash
            option_answer = serializer.save()

            # OptionAnswer ning to'g'riligini tekshirish
            option = option_answer.option
            is_correct = option_answer.option.is_correct
            option_answer.is_correct = is_correct
            option_answer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryResultAPIView(APIView):
    def get(self, request, category_id, format=None):
        user_id = request.query_params.get('user')

        if not user_id:
            return Response({"detail": "User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Category va foydalanuvchi uchun javoblarni olish
        category = Category.objects.get(id=category_id)
        marathons = Marathon.objects.filter(category=category)

        # Foydalanuvchi javoblarini olish
        answers = OptionAnswer.objects.filter(marathon__in=marathons, user_id=user_id)

        correct_answers = answers.filter(is_correct=True).count()
        incorrect_answers = answers.filter(is_correct=False).count()
        unanswered = marathons.count() * 3 - (correct_answers + incorrect_answers)  # Assumed 3 options per marathon
        total_questions = marathons.count() * 3

        if total_questions > 0:
            correct_percentage = (correct_answers / total_questions) * 100
        else:
            correct_percentage = 0

        return Response({
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "unanswered": unanswered,
            "correct_percentage": correct_percentage
        })


from django.contrib.auth import get_user_model
from exams.models import Marathon, Option, OptionAnswer

User = get_user_model()


class MarathonAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Foydalanuvchini tekshirish

    def post(self, request, marathon_id, format=None):
        user = request.user  # user ID ni requestdan olish
        option_id = request.data.get('option')
        text = request.data.get('text')

        if not option_id:
            return Response({"detail": "Option ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Marathonni tekshirish
        try:
            marathon = Marathon.objects.get(id=marathon_id)
        except Marathon.DoesNotExist:
            return Response({"detail": "Marathon not found"}, status=status.HTTP_404_NOT_FOUND)

        # Optionni tekshirish
        try:
            option = Option.objects.get(id=option_id, marathon=marathon)
        except Option.DoesNotExist:
            return Response({"detail": "Option not found in this marathon"}, status=status.HTTP_404_NOT_FOUND)

        # To‘g‘ri yoki noto‘g‘ri javob
        is_correct = option.is_correct

        # Javobni saqlash
        answer = OptionAnswer.objects.create(
            user=user,
            option=option,
            text=text,
            is_correct=is_correct,
            answered_at=timezone.now()
        )

        return Response({
            "user": user.id,
            "option": option.id,
            "text": text,
            "is_correct": is_correct,
            "answered_at": answer.answered_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, status=status.HTTP_201_CREATED)


class MarathonResultAPIView(APIView):
    def get(self, request, marathon_id, format=None):
        user_id = request.query_params.get("user")

        if not user_id:
            return Response({"detail": "User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)  # ID ni int formatga o'tkazish
        except ValueError:
            return Response({"detail": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Marafon mavjudligini tekshirish
        try:
            marathon = Marathon.objects.get(id=marathon_id)
        except Marathon.DoesNotExist:
            return Response({"detail": "Marathon not found"}, status=status.HTTP_404_NOT_FOUND)

        # Marafonga tegishli savollar sonini olish
        total_questions = Option.objects.filter(marathon=marathon).count()

        # Foydalanuvchining javoblarini olish
        answers = OptionAnswer.objects.filter(option__marathon=marathon, user_id=user_id)

        correct_answers = answers.filter(is_correct=True).count()
        incorrect_answers = answers.filter(is_correct=False).count()
        unanswered = total_questions - (correct_answers + incorrect_answers)

        correct_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        return Response({
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "unanswered": unanswered,
            "correct_percentage": round(correct_percentage, 2)
        })

class MarathonListAPIView(ListAPIView):
    queryset = Marathon.objects.all()
    serializer_class = MarathonSerializer


class MarathonDetailAPIView(RetrieveAPIView):
    queryset = Marathon.objects.all()
    serializer_class = MarathonSerializer
    lookup_field = 'id'