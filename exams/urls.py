from django.urls import path
from .views import CategoryDetailView, MarathonListView, UserResultsView, CategoryResultsAPIView

urlpatterns = [
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-list"),
    path("marathons/", MarathonListView.as_view(), name="marathon-list"),
    path("Marathon-answer/", UserResultsView.as_view(), name="submit-answer"),
    path("Category/", CategoryResultsAPIView.as_view(), name="submit-answer"),
]
