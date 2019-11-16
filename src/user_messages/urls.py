from django.urls import path
from .views import (
    MessageCreateView, MessageDetail, MessagesListAll)

app_name = "messages"

urlpatterns = [
    path('', MessagesListAll.as_view(), name="message-list"),
    path('write/', MessageCreateView.as_view(), name="message-write"),
    path('<pk>/', MessageDetail.as_view(), name="message-detail"),
]
