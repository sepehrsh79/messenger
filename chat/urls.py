from django.urls import path

from . import views


app_name = "chat"

urlpatterns = [
    path('doc/', views.document_view, name='doc'),
    path('<str:room_code>/', views.room, name='room'),
]
