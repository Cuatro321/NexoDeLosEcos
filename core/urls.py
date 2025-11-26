from django.urls import path
from .views import HomeView, OfflineView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('offline/', OfflineView.as_view(), name='offline'),
]
