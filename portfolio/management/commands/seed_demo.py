from django.core.management.base import BaseCommand
from portfolio.models import (Certificate, Project, ProjectCategory, ProjectFeature, ProjectFlowStep, Service,
                              SiteSettings, Skill, SocialLink, TypingText)

DOCS = [
    ("Project Overview", ["Project Title & Description", "Problem Statement", "Objectives", "Target Users", "Technology Stack"]),
    ("Requirements & Analysis", ["Functional Requirements", "Non-Functional Requirements", "User Roles & Permissions", "Feasibility Study"]),
    ("System Design & UI/UX", ["System Architecture", "Database Design (ER Diagram)", "Wireframes & Mockups", "User Flow Diagram", "Design System (Colors, Fonts)"]),
    ("Development & Implementation", ["Frontend Development", "Backend & APIs", "Authentication & Authorization", "Third-party Integrations", "Version Control (Git)"]),
    ("Testing & Deployment", ["Unit Testing", "Integration Testing", "Functional Testing", "UI Testing", "Bug Tracking", "Deployment Strategy",
                              "Hosting Platform", "Domain & SSL", "Backup & Recovery", "Maintenance"]),
    ("Business & Project Management", ["Project Scope", "Project Timeline", "Team Responsibilities", "Cost Estimation", "Risk Analysis",
                                       "Project Limitations", "Success Metrics (KPIs)", "Expected Results", "Future Scope"]),
]


class Command(BaseCommand):
    help = "Fill the site with demo content (safe to re-run)."

    def handle(self, *args, **opts):
        site, _ = SiteSettings.objects.get_or_create(pk=1, defaults={
            "phone": "+91 98765 43210", "location": "Srikakulam, India", "email": "hello@charlotte.dev"})
        if not site.typing_texts.exists():
            for i, w in enumerate(["Frontend Developer", "UI/UX Designer", "React Developer", "Django Developer"]):
                TypingText.objects.create(site=site, text=w, order=i)
        for i, (n, p, c, ic) in enumerate([("React JS", 90, "#38bdf8", "bi-filetype-jsx"), ("Tailwind CSS", 85, "#22d3ee", "bi-wind"),
                                           ("JavaScript", 92, "#facc15", "bi-filetype-js"), ("Django", 88, "#34d399", "bi-filetype-py"),
                                           ("Figma", 90, "#f472b6", "bi-figma")]):
            Skill.objects.get_or_create(name=n, defaults={"percent": p, "color": c, "icon": ic, "order": i})
        if not Certificate.objects.exists():
            for i, (o, t, ic) in enumerate([("Google", "Digital Skills Certificate", "bi-google"), ("Meta", "Front End Developer Certificate", "bi-meta"),
                                            ("Microsoft", "Azure Fundamentals", "bi-microsoft"), ("Udemy", "Python Programming", "bi-mortarboard-fill")]):
                Certificate.objects.create(issuer=o, title=t, logo_icon=ic, order=i)
        if not Service.objects.exists():
            for i, (t, d, ic) in enumerate([
                ("UI/UX Design", "Designing intuitive and beautiful user experiences.", "bi-vector-pen"),
                ("Frontend Development", "Building fast and interactive web applications.", "bi-code-slash"),
                ("Responsive Web Design", "Crafting websites that look great on all devices.", "bi-display")]):
                Service.objects.create(title=t, description=d, icon=ic, order=i)
        if not Project.objects.exists():
            p = Project.objects.create(
                title="Food Ordering App", description="Modern & Interactive UI", order=0,
                role_in_project="Designer & Developer", year="2025", tech_stack="React, Tailwind CSS, Django",
                problem_statement="Customers waste time calling restaurants and have no idea when their food will arrive.",
                solution="A responsive web app where users browse menus, pay online and track the order live.",
                outcome="Checkout time dropped by 40% in user testing.")
            for i, (t_, d, ic) in enumerate([("Live order tracking", "Real-time status from kitchen to door", "bi-geo-alt"),
                                             ("Secure payments", "Cards and UPI supported", "bi-shield-check"),
                                             ("Role based login", "Customer, restaurant and admin dashboards", "bi-people")]):
                ProjectFeature.objects.create(project=p, title=t_, description=d, icon=ic, order=i)
            for i, (t_, d, ty, lb) in enumerate([("Open app", "", "start", ""), ("Login / Sign up", "", "process", ""),
                                                 ("Logged in?", "", "decision", ""), ("Browse menu", "Add items to cart", "process", "Yes"),
                                                 ("Pay & track order", "", "process", ""), ("Order delivered", "", "end", "")]):
                ProjectFlowStep.objects.create(project=p, title=t_, description=d, step_type=ty, arrow_label=lb, order=i)
            Project.objects.create(title="Creative Design", description="Light & Dark mode UI", order=1)
            Project.objects.create(title="Responsive Dashboard", description="Responsive & Modern", order=2)
        first = Project.objects.first()
        if first and not first.categories.exists():
            for i, (title, items) in enumerate(DOCS):
                ProjectCategory.objects.create(project=first, title=title, items="\n".join(items), order=i)
        if not SocialLink.objects.exists():
            for i, p in enumerate(["instagram", "tiktok", "github", "youtube"]):
                SocialLink.objects.create(platform=p, url="https://example.com", order=i)
        self.stdout.write(self.style.SUCCESS("Demo content created. Upload images in /admin/."))
