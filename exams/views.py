from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Marathon, Option
from .serializers import CategorySerializer, MarathonSerializer, CategoryListSerializer
from rest_framework.permissions import IsAuthenticated




class MarathonListView(generics.ListAPIView):
    queryset = Marathon.objects.all()
    serializer_class = MarathonSerializer
    permission_classes = [IsAuthenticated]  # Ruxsat qo‘shildi



class UserResultsView(APIView):
    permission_classes = [IsAuthenticated]

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


class CategoryResultsAPIView(APIView):
    """Kategoriya bo‘yicha natijalarni hisoblash"""
    permission_classes = [IsAuthenticated]  # Foydalanuvchini tekshirish

    def post(self, request, *args, **kwargs):
        user = request.user  # Foydalanuvchini olish
        category_id = request.data.get("category_id")  # Kategoriya ID
        selected_option_ids = request.data.get("selected_options", [])  # Tanlangan variantlar ID-lari

        if not category_id:
            return Response({"error": "category_id talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        # Kategoriya mavjudligini tekshirish
        category = get_object_or_404(Category, id=category_id)

        # Ushbu kategoriya ichidagi marafonlarni olish
        marathons = Marathon.objects.filter(category=category)
        total_marathons = marathons.count()

        # Ushbu marafonlar ichidagi barcha savollarning variantlarini olish
        valid_options = Option.objects.filter(marathon__in=marathons)

        # **Kategoriya ichidagi umumiy savollar sonini hisoblash**
        total_questions = valid_options.values("marathon_id").distinct().count()

        # **Foydalanuvchi tanlagan variantlar faqat ushbu kategoriya ichida bo‘lishi kerak**
        selected_options = valid_options.filter(id__in=selected_option_ids)

        # **To‘g‘ri javoblarni hisoblash**
        correct_answers = selected_options.filter(is_correct=True).count()

        # **Foydalanuvchi nechta savolga javob berganligini hisoblash**
        answered_questions = selected_options.values("marathon_id").distinct().count()

        # **Noto‘g‘ri javoblar soni**
        incorrect_answers = answered_questions - correct_answers

        # **Tashlab ketilgan savollar soni**
        skipped_questions = total_questions - answered_questions

        # **To‘g‘ri javoblar foizi**
        correct_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

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


# class CategoryResultsAPIView(generics.CreateAPIView):
#     """Kategoriya bo‘yicha natijalarni hisoblash"""
#     permission_classes = [IsAuthenticated]  # Foydalanuvchini tekshirish
#
#     def create(self, request, *args, **kwargs):
#         user = request.user  # Foydalanuvchini olish
#         category_id = request.data.get("category_id")  # Kategoriya ID
#         selected_option_ids = request.data.get("selected_options", [])  # Tanlangan variantlar ID-lari
#
#         if not category_id:
#             return Response({"error": "category_id talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Kategoriya mavjudligini tekshirish
#         category = get_object_or_404(Category, id=category_id)
#
#         # Ushbu kategoriya ichidagi marafonlarni olish
#         marathons = Marathon.objects.filter(category=category)
#         total_marathons = marathons.count()
#
#         # Ushbu marafonlar ichidagi barcha savollarning variantlarini olish
#         valid_options = Option.objects.filter(marathon__in=marathons)
#
#         # Tanlangan variantlar faqat ushbu marafon va kategoriya ichida bo‘lishi kerak
#         selected_options = valid_options.filter(id__in=selected_option_ids)
#
#         # Kategoriya ichidagi umumiy savollar sonini hisoblash
#         total_questions = valid_options.values("marathon").distinct().count()
#
#         # Foydalanuvchi nechta savolga javob berganligini hisoblash
#         answered_questions = selected_options.values("marathon").distinct().count()
#
#         # To‘g‘ri va noto‘g‘ri javoblarni hisoblash
#         correct_answers = selected_options.filter(is_correct=True).count()
#         incorrect_answers = answered_questions - correct_answers
#
#         # Tashlab ketilgan savollarni hisoblash
#         skipped_questions = total_questions - answered_questions
#
#         # To‘g‘ri javoblar foizini hisoblash
#         correct_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
#
#         return Response({
#             "user_id": user.id,
#             "user_name": user.get_full_name() if user.get_full_name() else user.username,
#             "category_id": category.id,
#             "category_name": category.title,
#             "total_marathons": total_marathons,
#             "total_questions": total_questions,
#             "total_answered_questions": answered_questions,
#             "total_skipped_questions": skipped_questions,
#             "total_correct_answers": correct_answers,
#             "total_incorrect_answers": incorrect_answers,
#             "category_correct_percentage": round(correct_percentage, 2)
#         }, status=status.HTTP_200_OK)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#
# class SubmitTicketResultsAPIView(generics.CreateAPIView):
#     """Foydalanuvchining bilet natijalarini saqlash (POST)"""
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#         ticket_id = request.data.get("ticket_id")
#         selected_option_ids = request.data.get("selected_options", [])
#
#         if not ticket_id:
#             return Response({"error": "ticket_id talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user_ticket = UserTicket.objects.get(user=user, ticket_id=ticket_id)
#         except UserTicket.DoesNotExist:
#             return Response({"error": "Bunday bilet mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
#
#         UserTicketResult.objects.filter(user_ticket=user_ticket).delete()
#
#         selected_options = Option.objects.filter(id__in=selected_option_ids) if selected_option_ids else Option.objects.none()
#
#         user_result = UserTicketResult.objects.create(user_ticket=user_ticket)
#         user_result.calculate_results()
#
#         return Response({
#             "user_id": user.id,
#             "ticket_id": user_ticket.ticket.id,
#             "total_questions": user_ticket.ticket.questions.count(),
#             "total_answered_questions": selected_options.count(),
#             "total_skipped_questions": user_result.skipped_questions,
#             "total_correct_answers": user_result.correct_answers,
#             "total_incorrect_answers": user_result.incorrect_answers,
#             "correct_percentage": round(user_result.correct_percentage, 2),
#         }, status=status.HTTP_200_OK)