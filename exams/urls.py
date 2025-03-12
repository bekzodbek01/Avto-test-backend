from django.urls import path
from .views import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    OptionAnswerCreateAPIView,
    CategoryResultAPIView,
    CategoryAnswerAPIView,
    MarathonAnswerAPIView,
    MarathonResultAPIView,
    MarathonListAPIView,
    MarathonDetailAPIView
)

urlpatterns = [
    # Kategoriya API yo‘llari
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/result/', CategoryResultAPIView.as_view(), name='category-result'),
    path('categories/answer/', CategoryAnswerAPIView.as_view(), name='category-answer'),

    # Marafon API yo‘llari
    path('marathons/', MarathonListAPIView.as_view(), name='marathon-list'),
    path('marathons/<int:id>/', MarathonDetailAPIView.as_view(), name='marathon-detail'),
    path('marathons/<int:marathon_id>/result/', MarathonResultAPIView.as_view(), name='marathon-result'),
    path('marathons/answer/', MarathonAnswerAPIView.as_view(), name='marathon-answer'),

    # Variant tanlash API yo‘li
    path('option-answer/', OptionAnswerCreateAPIView.as_view(), name='option-answer'),
]
