from .forms import UserCreationFormWithEmail
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?registered'