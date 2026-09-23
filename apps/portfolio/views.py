from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import (
    Profile, Skill, Service, Experience, Education,
    Certificate, Project, SocialLink,
)
from .forms import ContactForm


def home(request):
    profile = Profile.objects.first()
    context = {
        "profile": profile,
        "skills": Skill.objects.all(),
        "services": Service.objects.all(),
        "experiences": Experience.objects.all(),
        "education": Education.objects.all(),
        "certificates": Certificate.objects.all(),
        "projects": Project.objects.all(),
        "social_links": SocialLink.objects.all(),
        "contact_form": ContactForm(),
        "meta_title": profile.full_name if profile else settings.SITE_NAME,
        "meta_description": profile.meta_description if profile else "",
    }
    return render(request, "home.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(pk=project.pk)[:3]
    context = {
        "project": project,
        "related_projects": related_projects,
        "meta_title": project.title,
        "meta_description": project.short_description,
    }
    return render(request, "project_detail.html", context)


def contact_submit(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send an email notification — failures here should never break the UX.
            try:
                subject = f"New portfolio message: {contact_message.subject or 'No subject'}"
                body = render_to_string("emails/contact_notification.txt", {
                    "contact_message": contact_message,
                })
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Thanks for reaching out! I'll get back to you soon.")
        else:
            messages.error(request, "Please fix the errors below and try again.")
            profile = Profile.objects.first()
            context = {
                "profile": profile,
                "skills": Skill.objects.all(),
                "services": Service.objects.all(),
                "experiences": Experience.objects.all(),
                "education": Education.objects.all(),
                "certificates": Certificate.objects.all(),
                "projects": Project.objects.all(),
                "social_links": SocialLink.objects.all(),
                "contact_form": form,
            }
            return render(request, "home.html", context)
    return redirect("/#contact")


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
