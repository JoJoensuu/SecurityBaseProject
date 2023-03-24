from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Note
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NoteForm
from django.db import connection
from django.http import HttpResponseRedirect


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class HomePageView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "home.html"
    context_object_name = "note_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("filter")
        if query:
            queryset = queryset.raw(f"SELECT * FROM notes_note WHERE text LIKE '%{query}%' AND user_id = {self.request.user.id}")
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
class CreateNoteView(generic.CreateView):
    form_class = NoteForm
    success_url = reverse_lazy("home")
    template_name = "create_note.html"

    def form_valid(self, form):
        text = form.cleaned_data['text']
        user_id = self.request.user.pk

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO notes_note (text, user_id) VALUES ("%s", %s)' % (text, user_id))
            print(connection.queries)
        
        return HttpResponseRedirect(reverse("home"))
    
class DeleteNoteView(UserPassesTestMixin, generic.DeleteView):
    model = Note
    success_url = reverse_lazy("home")
    template_name = "delete_note.html"

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user
