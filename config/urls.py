from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # Django Admin
    path("admin/", admin.site.urls),

    # Portfolio
    path("", include("apps.portfolio.urls")),

]


# Custom error pages
handler404 = "apps.portfolio.views.error_404"
handler500 = "apps.portfolio.views.error_500"


# Media files
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )