from django.urls import path
from .views import CategoryDetailView, MarathonListView, UserResultsView, CategoryResultsAPIView, CategoryListView

urlpatterns = [
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-list"),
    path("marathons/", MarathonListView.as_view(), name="marathon-list"),
    path("Marathon-answer/", UserResultsView.as_view(), name="submit-answer"),
    path("category-answer/", CategoryResultsAPIView.as_view(), name="submit-answer"),
    # path('ticket/<int:ticket_id>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    path("category/", CategoryListView.as_view(), name="submit-answer"),
]
