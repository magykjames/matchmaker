from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from questions.models import Question

from .forms import ContactForm, SignUpForm
from .models import SignUp

# Create your views here.
def home(request):
    title = "Sign Up Now"
    form = SignUpForm(request.POST or None)

    context = {
        "title": title,
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        print instance.email
        context = {
            "title": "Thank You"
        }

    if request.user.is_authenticated():
        queryset = Question.objects.all().order_by('-timestamp')
        context = {
            "queryset": queryset
        }
        return render(request, "questions/home.html", context)

    return render(request, "home.html", context)

def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')

        subject = 'Site Contact Form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'magykzan@gmail.com']
        contact_message = "%s: %s via %s"%(
            form_full_name,
            form_message,
            form_email
        )

        send_mail(
            subject,
            contact_message,
            from_email,
            to_email,
            fail_silently=False
        )
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "forms.html", context)
