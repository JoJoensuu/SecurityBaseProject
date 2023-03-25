from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Note
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NoteForm
from django.db import connection
from django.http import HttpResponseRedirect

# CSRF Vulnerability:
# When fixing vulnerability these imports are no longer needed.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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
            # SQL INJECTION VULNERABILITY:
            # Replace below queryset with
                # queryset = queryset.filter(text__icontains=query, user_id=self.request.user.id)
            # to fix vulnerability
            queryset = queryset.raw(f"SELECT * FROM notes_note WHERE text LIKE '%{query}%' AND user_id = {self.request.user.id}")
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset

            # BROKEN ACCESS CONTROL VULNERABILITY:
            # To fix add LoginRequiredMixin to CreateNoteView parameters.

class CreateNoteView(generic.CreateView):
    form_class = NoteForm
    success_url = reverse_lazy("home")
    template_name = "create_note.html"

            # CSRF VULNERABILITY:
            # Remove this method entirely to fix.

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        self.csrf_exempt = True
        return super().dispatch(*args, **kwargs)
    
            # SQL INJECTION VULNERABILITY:
            # Replace below form_valid function with
            # def form_valid(self, form):
            #   form.instance.user = self.request.user
            #   return super().form_valid(form)

    def form_valid(self, form):
        text = form.cleaned_data['text']
        user_id = self.request.user.pk

            # XSS VULNERABILITY:
            # To fix import escape from django.utils.html
            # Replace below cursor.execute with:
            # cursor.execute('INSERT INTO notes_note (text, user_id) VALUES ("%s", %s)' % (escape(text), user_id))
            # This will 'clean' the user input

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO notes_note (text, user_id) VALUES ("%s", %s)' % (text, user_id))
        
        return HttpResponseRedirect(reverse("home"))

class DeleteNoteView(UserPassesTestMixin, generic.DeleteView):
    model = Note
    success_url = reverse_lazy("home")
    template_name = "delete_note.html"

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user
