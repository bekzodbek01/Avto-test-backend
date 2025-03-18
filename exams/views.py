from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Marathon, Option, UserAnswer
from .serializers import UserAnswerSerializer, CategorySerializer, MarathonSerializer
from rest_framework.permissions import IsAuthenticated


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MarathonListView(generics.ListAPIView):
    queryset = Marathon.objects.all()
    serializer_class = MarathonSerializer


class UserResultsView(APIView):
    def post(self, request):
        user = request.user
        total_marathons = Marathon.objects.count()  # Umumiy marafonlar soni
        selected_option_ids = request.data.get("selected_options", [])  # Tanlangan variantlar

        # ✅ **Foydalanuvchi tanlagan variantlar sonini olish**
        total_selected_options = len(selected_option_ids)

        # ✅ **Foydalanuvchi tanlagan variantlarni olish**
        # Faqat mavjud variantlar olish
        selected_options = Option.objects.filter(id__in=selected_option_ids)

        # Tanlangan variantlar sonini hisoblash
        total_selected_options = selected_options.count()

        # ✅ **To‘g‘ri variantlar soni**
        correct_answers = selected_options.filter(is_correct=True).count()

        # ✅ **Noto‘g‘ri variantlar soni**:
        incorrect_answers = total_selected_options - correct_answers

        # ✅ **Tashlab ketilgan savollar soni**
        skipped_questions = max(total_marathons - total_selected_options, 0)

        # ✅ **To‘g‘ri javoblar foizi (0-100%)**
        correct_percentage = (correct_answers / total_marathons) * 100 if total_marathons else 0

        return Response({
            "user_id": user.id,
            "user_name": user.get_full_name() if user.get_full_name() else user.username,
            "total_marathons": total_marathons,  # Jami marafonlar soni
            "answered_questions": total_selected_options,  # Tanlangan variantlar soni
            "skipped_questions": skipped_questions,  # Tashlab ketilgan savollar soni
            "correct_answers": correct_answers,  # To‘g‘ri variantlar soni
            "incorrect_answers": incorrect_answers,  # Noto‘g‘ri variantlar soni
            "correct_percentage": round(min(correct_percentage, 100), 2)  # Foiz (100% dan oshmasligi)
        }, status=status.HTTP_200_OK)


class CategoryResultsAPIView(generics.CreateAPIView):
    """Kategoriya bo‘yicha natijalarni hisoblash"""
    permission_classes = [IsAuthenticated]  # Foydalanuvchini tekshirish

    def create(self, request, *args, **kwargs):
        user = request.user  # Foydalanuvchini olish
        category_id = request.data.get("category_id")  # Kategoriya ID
        selected_option_ids = request.data.get("selected_options", [])  # Tanlangan variantlar ID-lari

        if not category_id:
            return Response({"error": "category_id talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        # Kategoriya mavjudligini tekshirish
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # Kategoriya ichidagi marafonlarni olish
        marathons = Marathon.objects.filter(category=category)
        total_marathons = marathons.count()

        # Kategoriya ichidagi barcha savollar sonini hisoblash
        total_questions = Option.objects.filter(marathon__in=marathons).values("marathon").distinct().count()

        # Foydalanuvchi tanlagan variantlarni olish
        if selected_option_ids:
            selected_options = Option.objects.filter(id__in=selected_option_ids)
        else:
            selected_options = Option.objects.none()  # Hech qanday variant tanlanmagan bo'lsa

        # Foydalanuvchi nechta savolga javob berganligini hisoblash
        answered_questions = selected_options.values("marathon").distinct().count()

        # To‘g‘ri va noto‘g‘ri javoblarni hisoblash
        correct_answers = selected_options.filter(is_correct=True).count()
        incorrect_answers = answered_questions - correct_answers

        # Tashlab ketilgan savollarni hisoblash
        skipped_questions = total_questions - answered_questions

        # To‘g‘ri javoblar foizini hisoblash
        correct_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        # **Foydalanuvchi javoblarini saqlash**
        # Foydalanuvchining mavjud javobini olish yoki yangi yaratish
        user_answer = UserAnswer.objects.filter(user=user).first()
        if not user_answer:
            user_answer = UserAnswer.objects.create(user=user)

        user_answer.selected_options.set(selected_options)
        user_answer.is_correct = correct_answers > incorrect_answers
        user_answer.save()

        return Response({
            "user_id": user.id,
            "user_name": user.get_full_name() if user.get_full_name() else user.username,
            "category_id": category.id,
            "category_name": category.title,
            "total_marathons": total_marathons,
            "total_questions": total_questions,
            "total_answered_questions": answered_questions,
            "total_skipped_questions": skipped_questions,
            "total_correct_answers": correct_answers,
            "total_incorrect_answers": incorrect_answers,
            "category_correct_percentage": round(correct_percentage, 2)
        }, status=status.HTTP_200_OK)