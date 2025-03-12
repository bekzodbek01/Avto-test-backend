from .views import CategoryListAPIView, CategoryDetailAPIView, MarathonListAPIView, MarathonDetailAPIView
from django.urls import path
from .views import (
    MarathonResultAPIView,
    MarathonAnswerAPIView,
    OptionAnswerCreateAPIView,
    CategoryResultAPIView,
)

urlpatterns = [
    path('marathon/<int:marathon_id>/answer/', MarathonAnswerAPIView.as_view(), name='marathon-answer'),
    path('marathon/<int:marathon_id>/result/', MarathonResultAPIView.as_view(), name='marathon-result'),

    path('marathons/', MarathonListAPIView.as_view(), name='marathon-list'),
    path('marathon/<int:id>/', MarathonDetailAPIView.as_view(), name='marathon-detail'),

    path('option-answer/', OptionAnswerCreateAPIView.as_view(), name='option-answer-create'),
    path('category/<int:category_id>/results/', CategoryResultAPIView.as_view(), name='category-result'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),
]

