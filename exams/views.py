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
            option = serializer.validated_data['option']
            is_correct = option.is_correct  # Variant to‘g‘riligini olish
            serializer.validated_data['is_correct'] = is_correct
            option_answer = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryResultAPIView(APIView):
    def get(self, request, category_id, format=None):
        user_id = request.query_params.get('user')

        if not user_id or not user_id.isdigit():
            return Response({"detail": "Valid User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = int(user_id)
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        marathons = Marathon.objects.filter(category=category)
        total_questions = Option.objects.filter(marathon__in=marathons).count()
        answers = OptionAnswer.objects.filter(option__marathon__in=marathons, user_id=user_id)
        correct_answers = answers.filter(is_correct=True).count()
        incorrect_answers = answers.filter(is_correct=False).count()
        unanswered = total_questions - (correct_answers + incorrect_answers)

        correct_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        return Response({
            "category": {
                "id": category.id,
                "title": category.title
            },
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "unanswered": unanswered,
            "correct_percentage": round(correct_percentage, 2)
        })


class CategoryAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        option_id = request.data.get("option")

        if not option_id:
            return Response({"detail": "Option is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            option = Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            return Response({"detail": "Option not found"}, status=status.HTTP_404_NOT_FOUND)

        answer = OptionAnswer.objects.create(user=user, option=option, is_correct=option.is_correct)

        return Response({
            "message": "Answer saved successfully",
            "is_correct": answer.is_correct,
            "text": answer.text
        }, status=status.HTTP_201_CREATED)


class MarathonAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Autentifikatsiyadan o‘tgan foydalanuvchi
        option_id = request.data.get("option")

        if not option_id:
            return Response({"detail": "Option is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            option = Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            return Response({"detail": "Option not found"}, status=status.HTTP_404_NOT_FOUND)

        answer = OptionAnswer.objects.create(user=user, option=option, is_correct=option.is_correct)

        return Response({
            "message": "Answer saved successfully",
            "is_correct": answer.is_correct,
            "text": answer.text
        }, status=status.HTTP_201_CREATED)


class MarathonResultAPIView(APIView):
    def get(self, request, marathon_id, format=None):
        user_id = request.query_params.get("user")

        if not user_id or not user_id.isdigit():
            return Response({"detail": "Valid User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = int(user_id)
        try:
            marathon = Marathon.objects.get(id=marathon_id)
        except Marathon.DoesNotExist:
            return Response({"detail": "Marathon not found"}, status=status.HTTP_404_NOT_FOUND)

        total_questions = Option.objects.filter(marathon=marathon).count()
        answers = OptionAnswer.objects.filter(option__marathon=marathon, user_id=user_id)
        correct_answers = answers.filter(is_correct=True).count()
        incorrect_answers = answers.filter(is_correct=False).count()
        unanswered = total_questions - (correct_answers + incorrect_answers)

        correct_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        return Response({
            "total_questions": total_questions,
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