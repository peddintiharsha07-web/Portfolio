from django.db import models
from django.urls import reverse


class SiteSettings(models.Model):
    """Single record that controls all the text, images and theme of the site."""
    MODES = [("dark", "Dark"), ("light", "Light")]
    COLORS = [("red", "Crimson Red"), ("blue", "Ocean Blue"), ("green", "Emerald Green"), ("yellow", "Sunshine Yellow"),
              ("purple", "Royal Purple"), ("orange", "Sunset Orange"), ("pink", "Rose Pink")]

    # Branding / theme
    site_title = models.CharField(max_length=100, default="Charlotte | Frontend Developer")
    logo_text = models.CharField(max_length=6, default="PH", help_text="Short letters shown in the logo")
    default_mode = models.CharField(max_length=10, choices=MODES, default="dark")
    default_color = models.CharField(max_length=10, choices=COLORS, default="red")

    meta_description = models.CharField(max_length=160, blank=True, help_text="Shown in Google search results")
    show_mode_toggle = models.BooleanField(default=True, help_text="Let visitors switch light/dark mode")

    # Section switches & headings
    show_about = models.BooleanField(default=True)
    show_skills = models.BooleanField(default=True)
    show_certificates = models.BooleanField(default=True)
    show_projects = models.BooleanField(default=True)
    show_services = models.BooleanField(default=True)
    skills_title = models.CharField(max_length=40, default="My")
    skills_highlight = models.CharField(max_length=40, default="Skills")
    certificates_title = models.CharField(max_length=40, default="My")
    certificates_highlight = models.CharField(max_length=40, default="Certificates")
    projects_title = models.CharField(max_length=40, default="My Creative")
    projects_highlight = models.CharField(max_length=40, default="Projects")
    services_title = models.CharField(max_length=40, default="What I")
    services_highlight = models.CharField(max_length=40, default="Do")

    # Hero
    name = models.CharField(max_length=80, default="Charlotte")
    role = models.CharField(max_length=80, default="Frontend Developer", help_text="Fallback when no typing texts are added")
    availability_text = models.CharField(max_length=60, default="Available for work", blank=True)
    intro = models.TextField(default="I craft beautiful and responsive web experiences with modern technologies.")
    years_experience = models.CharField(max_length=10, default="2+")
    projects_done = models.CharField(max_length=10, default="15+")
    happy_clients = models.CharField(max_length=10, default="10+")
    cv_file = models.FileField(upload_to="cv/", blank=True, help_text="PDF used by the Download CV button")
    hero_image = models.ImageField(upload_to="images/", blank=True)

    # About
    about_title = models.CharField(max_length=80, default="Turning Ideas Into")
    about_highlight = models.CharField(max_length=80, default="Digital Reality")
    about_text = models.TextField(default="I'm a passionate Frontend Developer dedicated to creating exceptional digital experiences.")
    about_image = models.ImageField(upload_to="images/", blank=True)

    # Section images / headings
    skills_image = models.ImageField(upload_to="images/", blank=True, help_text="Illustration shown beside the skill tiles")
    skills_subtitle = models.CharField(max_length=200, default="Technologies and tools I work with to build amazing digital experiences.")
    certificate_image = models.ImageField(upload_to="images/", blank=True)
    certificates_subtitle = models.CharField(max_length=200, default="Continuous learning is the key to growth.")
    keep_learning_text = models.CharField(max_length=40, default="Keep Learning!", blank=True, help_text="Handwritten note beside the certificate image")
    projects_label = models.CharField(max_length=40, default="My Work", blank=True)
    services_badge = models.CharField(max_length=40, default="My Work", blank=True)
    services_subtitle = models.CharField(max_length=200, default="I bring ideas to life with modern technologies and creative design.")

    # Contact
    contact_title = models.CharField(max_length=80, default="Let's Work")
    contact_highlight = models.CharField(max_length=80, default="Together")
    contact_text = models.CharField(max_length=200, default="Have a project in mind or just want to say hi? Feel free to reach out!")
    email = models.EmailField(default="hello@example.com")
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    contact_image = models.ImageField(upload_to="images/", blank=True)
    footer_text = models.CharField(max_length=120, default="Made with ❤ and passion.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site settings"


class TypingText(models.Model):
    """Words that are typed one after another in the hero (Frontend Developer -> UI/UX Designer ...)."""
    site = models.ForeignKey(SiteSettings, related_name="typing_texts", on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class SocialLink(models.Model):
    PLATFORMS = [("instagram", "Instagram"), ("tiktok", "TikTok"), ("github", "GitHub"),
                 ("youtube", "YouTube"), ("linkedin", "LinkedIn"), ("twitter-x", "X / Twitter"),
                 ("facebook", "Facebook"), ("dribbble", "Dribbble"), ("behance", "Behance")]
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.get_platform_display()


class Skill(models.Model):
    name = models.CharField(max_length=50)
    percent = models.PositiveIntegerField(default=80, help_text="0 - 100")
    icon_image = models.ImageField(upload_to="skills/", blank=True, help_text="Logo image (best). Leave empty to use the icon class below")
    icon = models.CharField(max_length=40, default="bi-code-slash", help_text="Bootstrap Icons class, e.g. bi-filetype-js, bi-figma, bi-wind")
    color = models.CharField(max_length=7, default="#38bdf8", help_text="Icon / glow colour, e.g. #38bdf8")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Certificate(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Digital Skills Certificate")
    issuer = models.CharField(max_length=100, help_text="e.g. Google")
    logo = models.ImageField(upload_to="certificates/", blank=True, help_text="Issuer logo. Leave empty to use the icon class below")
    logo_icon = models.CharField(max_length=40, default="bi-award-fill", help_text="Bootstrap Icons class, e.g. bi-google, bi-microsoft")
    status = models.CharField(max_length=30, default="Completed")
    year = models.CharField(max_length=4, blank=True)
    verify_url = models.URLField(blank=True, help_text="Opens when the card is clicked")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.issuer} - {self.title}"


class Project(models.Model):
    # Card info
    title = models.CharField(max_length=100)
    description = models.CharField("Short description", max_length=200, blank=True)
    image = models.ImageField("Cover image", upload_to="projects/", blank=True)
    order = models.PositiveIntegerField(default=0)
    # Case study
    role_in_project = models.CharField(max_length=80, blank=True, help_text="e.g. Designer & Developer")
    year = models.CharField(max_length=10, blank=True)
    tech_stack = models.CharField(max_length=200, blank=True, help_text="Comma separated: React, Tailwind, Django")
    problem_statement = models.TextField(blank=True, help_text="What problem does this project solve?")
    solution = models.TextField(blank=True, help_text="How did you solve it?")
    outcome = models.TextField("Outcome / results", blank=True)
    link = models.URLField("Live demo URL", blank=True)
    github_url = models.URLField("GitHub URL", blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.pk])

    @property
    def tech_list(self):
        return [x.strip() for x in self.tech_stack.split(",") if x.strip()]


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=40, default="bi-check-circle", help_text="Bootstrap Icons class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class ProjectFlowStep(models.Model):
    """One box of the user-flow diagram. Steps are drawn in order with arrows between them."""
    TYPES = [("start", "Start"), ("process", "Step / Screen"), ("decision", "Decision"), ("end", "End")]
    project = models.ForeignKey(Project, related_name="flow_steps", on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=120, blank=True)
    step_type = models.CharField(max_length=10, choices=TYPES, default="process")
    arrow_label = models.CharField(max_length=20, blank=True, help_text="Text on the arrow coming INTO this step, e.g. Yes / No")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class ProjectCategory(models.Model):
    """A numbered block on the project page, e.g. '5. Testing & Deployment' with a list of items."""
    project = models.ForeignKey(Project, related_name="categories", on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=True, blank=True, help_text="Leave empty to auto-number 1, 2, 3...")
    title = models.CharField(max_length=100)
    items = models.TextField(help_text="One item per line. Optional description: Item title | short description")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "project categories"

    def __str__(self):
        return self.title

    @property
    def item_list(self):
        out = []
        for line in self.items.splitlines():
            if line.strip():
                title, _, desc = line.partition("|")
                out.append({"title": title.strip(), "desc": desc.strip()})
        return out


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class Service(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=40, default="bi-code-slash",
                            help_text="Bootstrap Icons class, e.g. bi-code-slash (see icons.getbootstrap.com)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
