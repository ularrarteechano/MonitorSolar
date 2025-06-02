from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactFrom

# Create your views here.
def contact(request):
    contact_form = ContactFrom()
    if request.method == 'POST':
        contact_form = ContactFrom(data=request.POST)
        if contact_form.is_valid():
            email = EmailMessage(
               "asunto",
               "cuerpo",
               "no-contestar@prueba.com",
               ["prueba@prueba.com"],
            )
            try:
                email.send()
                return redirect(reverse('contact')+'?ok')
            except:
                return redirect(reverse('contact')+'?fail')
    return render(request, 'contact/contact.html', {'form': contact_form})