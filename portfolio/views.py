from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Certificate, Project, Service, SiteSettings, Skill


def home(request):
    site = SiteSettings.objects.get(pk=1) if SiteSettings.objects.exists() else SiteSettings.objects.create(pk=1)
    words = [t.text for t in site.typing_texts.all()] or [site.role]
    return render(request, "portfolio/home.html", {
        "skills": Skill.objects.all(),
        "certificates": Certificate.objects.all(),
        "projects": Project.objects.all(),
        "services": Service.objects.all(),
        "typing_words": words,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    ids = list(Project.objects.values_list("pk", flat=True))
    i = ids.index(project.pk)
    return render(request, "portfolio/project_detail.html", {
        "p": project,
        "categories": project.categories.all(),
        "features": project.features.all(),
        "flow": project.flow_steps.all(),
        "gallery": project.gallery.all(),
        "prev": Project.objects.filter(pk=ids[i - 1]).first() if i > 0 else None,
        "next": Project.objects.filter(pk=ids[i + 1]).first() if i < len(ids) - 1 else None,
    })


@require_POST
def set_color(request):
    """Only logged-in admins can change the site colour; it is saved for every visitor."""
    if not request.user.is_staff:
        return JsonResponse({"ok": False}, status=403)
    color = request.POST.get("color")
    if color not in dict(SiteSettings.COLORS):
        return JsonResponse({"ok": False}, status=400)
    site, _ = SiteSettings.objects.get_or_create(pk=1)
    site.default_color = color
    site.save()
    return JsonResponse({"ok": True})
