from django.contrib import admin
from .models import (Certificate, Project, ProjectFeature, ProjectFlowStep, ProjectImage, ProjectCategory,
                     Service, SiteSettings, Skill, SocialLink, TypingText)


class TypingTextInline(admin.TabularInline):
    model = TypingText
    extra = 1
    verbose_name = "Typing text (hero animation)"
    verbose_name_plural = "Typing texts - add, remove or reorder the animated words"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [TypingTextInline]
    fieldsets = (
        ("Branding & theme", {"fields": ("site_title", "meta_description", "logo_text", "default_mode",
                                         "default_color", "show_mode_toggle")}),
        ("Show / hide sections", {"fields": ("show_about", "show_skills", "show_certificates",
                                             "show_projects", "show_services")}),
        ("Hero", {"fields": ("name", "role", "availability_text", "intro", "years_experience",
                             "projects_done", "happy_clients", "cv_file", "hero_image")}),
        ("About", {"fields": ("about_title", "about_highlight", "about_text", "about_image")}),
        ("Section headings", {"fields": (("skills_title", "skills_highlight"), "skills_subtitle", "skills_image",
                                         ("certificates_title", "certificates_highlight"), "certificates_subtitle", "keep_learning_text", "certificate_image",
                                         "projects_label", ("projects_title", "projects_highlight"),
                                         "services_badge", ("services_title", "services_highlight"), "services_subtitle")}),
        ("Contact & footer", {"fields": ("contact_title", "contact_highlight", "contact_text", "email",
                                         "phone", "location", "contact_image", "footer_text")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(OrderedAdmin):
    list_display = ("platform", "url", "order")


@admin.register(Skill)
class SkillAdmin(OrderedAdmin):
    list_display = ("name", "percent", "icon", "color", "order")


@admin.register(Certificate)
class CertificateAdmin(OrderedAdmin):
    list_display = ("issuer", "title", "status", "order")


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ("title", "icon", "order")


class FeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    verbose_name_plural = "Key features - what the project includes"


class FlowInline(admin.TabularInline):
    model = ProjectFlowStep
    extra = 1
    verbose_name_plural = "User flow diagram steps (drawn in this order)"


class GalleryInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    verbose_name_plural = "Screenshots"


class CategoryInline(admin.StackedInline):
    model = ProjectCategory
    extra = 1
    fields = ("number", "title", "items", "order")
    verbose_name_plural = "Case study sections - add only the sections relevant to this project"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "items" and formfield:
            formfield.help_text = (
                "One item per line. Optional format: Item title | short explanation. "
                "Suggested sections: Target Audience, Research & Insights, User Persona, "
                "User Journey, Information Architecture, Wireframes, Visual Design, "
                "Challenges & Solutions, Testing, Results & Learnings. Leave a section out "
                "if it does not apply; empty sections are not shown on the case-study page."
            )
        return formfield


@admin.register(Project)
class ProjectAdmin(OrderedAdmin):
    list_display = ("title", "year", "order")
    inlines = [CategoryInline, FeatureInline, FlowInline, GalleryInline]
    fieldsets = (
        ("Card (shown on the home page)", {"fields": ("title", "description", "image", "order")}),
        ("Case study details", {"fields": ("role_in_project", "year", "tech_stack", "problem_statement",
                                           "solution", "outcome")}),
        ("Links", {"fields": ("link", "github_url")}),
    )
