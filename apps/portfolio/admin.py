from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile, SocialLink, Skill, Service, Experience, Education,
    Certificate, Project, ProjectImage, ContactMessage,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_title", "available_for_work")
    fieldsets = (
        ("Hero Section", {
            "fields": (
                "full_name", "role_title", "tagline", "short_intro",
                "available_for_work", "profile_image", "resume",
                ("projects_completed", "years_experience", "happy_clients"),
            )
        }),
        ("About Section", {
            "fields": ("about_badge", "about_heading", "about_description", "about_image")
        }),
        ("Contact Info", {
            "fields": ("email", "phone", "location")
        }),
        ("SEO / Open Graph", {
            "fields": ("meta_description", "og_image")
        }),
    )

    def has_add_permission(self, request):
        # enforce a single Profile row
        return not Profile.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order")
    list_editable = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage", "order")
    list_editable = ("percentage", "order")
    ordering = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "order")
    list_editable = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "is_current", "order")
    list_editable = ("order",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_year", "end_year", "order")
    list_editable = ("order",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "issuing_organization", "year", "order")
    list_editable = ("order",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "thumbnail_preview")
    list_editable = ("featured", "order")
    list_filter = ("category", "featured")
    search_fields = ("title", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ("Card Info", {
            "fields": (
                "title", "slug", "short_description", "category", "technologies",
                "thumbnail", "live_url", "github_url", "figma_url",
                ("featured", "order"),
            )
        }),
        ("Case Study", {
            "classes": ("collapse",),
            "fields": (
                "hero_image", "overview", "problem", "research", "user_personas",
                "user_flow", "wireframes", "ui_design", "design_system",
                "development", "challenges", "solution", "final_result",
                "prototype_url",
            )
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.thumbnail.url)
        return "-"
    thumbnail_preview.short_description = "Preview"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def has_add_permission(self, request):
        return False


admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your portfolio content"
