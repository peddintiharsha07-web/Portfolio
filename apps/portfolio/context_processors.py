from django.conf import settings
from .models import Profile, SocialLink


def site_context(request):
    """Makes profile + social links available in every template (nav, footer)."""
    profile = Profile.objects.first()
    social_links = SocialLink.objects.all()
    return {
        "site_name": settings.SITE_NAME,
        "global_profile": profile,
        "global_social_links": social_links,
    }
