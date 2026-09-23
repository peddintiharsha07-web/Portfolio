from django.core.management.base import BaseCommand
from apps.portfolio.models import (
    Profile, Skill, Service, Experience, Education,
    Certificate, Project, SocialLink,
)


class Command(BaseCommand):
    help = "Seed the database with demo portfolio content so the site isn't empty on first run."

    def handle(self, *args, **options):
        if not Profile.objects.exists():
            Profile.objects.create(
                full_name="Alex Rivera",
                role_title="UI/UX Designer & Full Stack Developer",
                tagline="Designing clean interfaces, building solid backends.",
                short_intro=(
                    "I design intuitive interfaces and build the full-stack products "
                    "behind them — from Figma file to production-ready Django app."
                ),
                available_for_work=True,
                projects_completed=32,
                years_experience=4,
                happy_clients=18,
                about_heading="Turning Ideas Into Digital Experiences",
                about_description=(
                    "I bridge the gap between design and engineering. Every project starts "
                    "with understanding the user, moves through wireframes and prototypes, "
                    "and ends as a fast, accessible, production-ready product."
                ),
                email="hello@example.com",
                location="Remote",
                meta_description="Portfolio of a UI/UX designer and full-stack developer.",
            )
            self.stdout.write(self.style.SUCCESS("Created Profile"))

        socials = [
            ("instagram", "https://instagram.com/yourhandle"),
            ("linkedin", "https://linkedin.com/in/yourhandle"),
            ("github", "https://github.com/yourhandle"),
            ("behance", "https://behance.net/yourhandle"),
        ]
        for i, (platform, url) in enumerate(socials):
            SocialLink.objects.get_or_create(platform=platform, defaults={"url": url, "order": i})

        skills = [
            ("Figma", 92, "bi-vector-pen"), ("UI/UX Design", 90, "bi-palette2"),
            ("React.js", 82, "bi-filetype-jsx"), ("JavaScript", 85, "bi-filetype-js"),
            ("HTML", 95, "bi-filetype-html"), ("CSS", 90, "bi-filetype-css"),
            ("Django", 88, "bi-server"), ("Python", 90, "bi-filetype-py"),
            ("Node.js", 70, "bi-hdd-network"), ("MongoDB", 68, "bi-database"),
            ("Git/GitHub", 85, "bi-git"),
        ]
        for i, (name, pct, icon) in enumerate(skills):
            Skill.objects.get_or_create(name=name, defaults={"percentage": pct, "icon_class": icon, "order": i})

        services = [
            ("UI/UX Design", "Wireframes, prototypes and polished interfaces rooted in user research.", "bi-palette"),
            ("Web Design", "Modern, on-brand websites designed for clarity and conversion.", "bi-layout-text-window"),
            ("Frontend Development", "Pixel-accurate, responsive interfaces built with clean code.", "bi-code-slash"),
            ("Full Stack Development", "End-to-end products — from database schema to deployed UI.", "bi-diagram-3"),
            ("Django Development", "Secure, scalable backends and admin-managed content.", "bi-braces-asterisk"),
            ("Responsive Design", "Interfaces that feel native on every screen size.", "bi-phone"),
        ]
        for i, (title, desc, icon) in enumerate(services):
            Service.objects.get_or_create(title=title, defaults={"description": desc, "icon_class": icon, "order": i})

        certs = [
            ("Google UX Design Certificate", "Google / Coursera", 2023, "https://coursera.org"),
            ("Meta Front-End Developer", "Meta / Coursera", 2022, "https://coursera.org"),
            ("Django for Everybody", "University of Michigan", 2021, "https://coursera.org"),
        ]
        for i, (name, org, year, url) in enumerate(certs):
            Certificate.objects.get_or_create(
                name=name, defaults={"issuing_organization": org, "year": year, "verification_url": url, "order": i}
            )

        projects = [
            ("Flona AI", "AI-powered plant care assistant with a clean mobile-first UI.", "uiux", "Figma, React, Node.js"),
            ("Digital Medical Record Management System", "Secure records portal for clinics with role-based access.", "fullstack", "Django, PostgreSQL, HTMX"),
            ("Personalized Learning Platform", "Adaptive course platform with progress tracking.", "web", "React, Django REST, Tailwind"),
            ("Government Services / License App UI", "Simplified UI concept for renewing licenses online.", "uiux", "Figma, Design System"),
            ("Food Delivery UI", "End-to-end ordering experience with live tracking.", "mobile", "Figma, React Native"),
            ("Transportation App UI", "Ride booking flow focused on speed and trust.", "mobile", "Figma, Prototype"),
            ("Personal Portfolio", "This very site — Django-powered and fully admin-editable.", "fullstack", "Django, Bootstrap, JS"),
        ]
        for i, (title, short_desc, cat, tech) in enumerate(projects):
            Project.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": short_desc,
                    "category": cat,
                    "technologies": tech,
                    "featured": i < 3,
                    "order": i,
                    "overview": short_desc,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed data created. Note: add images via /admin/ for thumbnails/profile photos."))
