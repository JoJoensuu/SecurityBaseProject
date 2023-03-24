from django.urls import path
from .views import SignUpView, HomePageView, CreateNoteView, DeleteNoteView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", HomePageView.as_view(), name="home"),
    path("create-note/", CreateNoteView.as_view(), name="create_note"),
    path("delete-note/<int:pk>/", DeleteNoteView.as_view(), name="delete_note"),
]