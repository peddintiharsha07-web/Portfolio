from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    """Singleton-style model holding the hero / global profile info."""

    full_name = models.CharField(max_length=120)
    role_title = models.CharField(
        max_length=200, help_text="e.g. UI/UX Designer & Full Stack Developer"
    )
    tagline = models.CharField(max_length=255, blank=True)
    short_intro = models.TextField(help_text="Short paragraph shown in the hero section.")
    available_for_work = models.BooleanField(default=True)

    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    about_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True)

    projects_completed = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)

    about_badge = models.CharField(max_length=60, default="ABOUT ME")
    about_heading = models.CharField(
        max_length=200, default="Turning Ideas Into Digital Experiences"
    )
    about_description = models.TextField(blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)

    meta_description = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to="meta/", blank=True, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # keep this a de-facto singleton
        if not self.pk and Profile.objects.exists():
            self.pk = Profile.objects.first().pk
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("behance", "Behance"),
        ("twitter", "Twitter / X"),
        ("dribbble", "Dribbble"),
        ("other", "Other"),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(
        max_length=60,
        blank=True,
        help_text="Optional bootstrap-icons class override, e.g. 'bi-instagram'",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.get_platform_display()

    def default_icon(self):
        mapping = {
            "instagram": "bi-instagram",
            "linkedin": "bi-linkedin",
            "github": "bi-github",
            "behance": "bi-behance",
            "twitter": "bi-twitter-x",
            "dribbble": "bi-dribbble",
            "other": "bi-link-45deg",
        }
        return self.icon_class or mapping.get(self.platform, "bi-link-45deg")


class Skill(models.Model):
    name = models.CharField(max_length=80)
    percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Honest proficiency 0-100. Avoid inflating this number.",
    )
    icon_class = models.CharField(
        max_length=60, blank=True, help_text="Optional bootstrap-icons class, e.g. 'bi-figma'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-percentage"]

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=60, default="bi-palette", help_text="Bootstrap-icons class"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Experience(models.Model):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    verification_url = models.URLField(blank=True)
    icon_class = models.CharField(max_length=60, default="bi-patch-check", blank=True)
    certificate_image = models.ImageField(upload_to="certificates/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year"]

    def __str__(self):
        return f"{self.name} ({self.year})"


class Project(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("uiux", "UI/UX Design"),
        ("web", "Web Development"),
        ("fullstack", "Full Stack"),
        ("mobile", "Mobile App UI"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="uiux")
    technologies = models.CharField(
        max_length=255, help_text="Comma-separated, e.g. Figma, React, Django"
    )
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True, null=True)

    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    figma_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    # --- Case study fields ---
    hero_image = models.ImageField(upload_to="projects/hero/", blank=True, null=True)
    overview = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    research = models.TextField(blank=True)
    user_personas = models.TextField(blank=True)
    user_flow = models.ImageField(upload_to="projects/user_flow/", blank=True, null=True)
    wireframes = models.TextField(blank=True)
    ui_design = models.TextField(blank=True)
    design_system = models.TextField(blank=True)
    development = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    final_result = models.TextField(blank=True)
    prototype_url = models.URLField(blank=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Project.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or 'No subject'}"
