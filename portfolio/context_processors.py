from .models import SiteSettings, SocialLink


def site(request):
    s, _ = SiteSettings.objects.get_or_create(pk=1)
    return {"s": s, "socials": SocialLink.objects.all(), "color_choices": SiteSettings.COLORS}
