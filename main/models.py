import uuid
from django.db import models
from django.contrib.auth.models import User


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, default="full-time"
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Education(models.Model):  ##new model untuk tugas 2
    LEVEL_CHOICES = [
        ("junior-high", "Junior High School"),
        ("senior-high", "Senior High School"),
        ("undergraduate", "Undergraduate"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    institution = models.CharField(max_length=255)

    level = models.CharField(
        max_length=30,
        choices=LEVEL_CHOICES,
    )

    entry_year = models.PositiveIntegerField()
    graduation_year = models.PositiveIntegerField()

    gpa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    utbk_score = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    logo_path = models.CharField(
        max_length=255,
        blank=True,
    )

    experience_anchor = models.SlugField(
        max_length=30,
        unique=True,
    )

    order = models.PositiveIntegerField(default=0)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.institution

    class Meta:
        ordering = ["order", "entry_year"]


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)

    starred_by = models.ManyToManyField(
        User,
        related_name="starred_projects",
        blank=True,
    )

    def __str__(self):
        return self.title


class Skill(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    logo_url = models.URLField(
        blank=True,
        max_length=500,
    )

    description = models.TextField(
        blank=True,
    )

    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="skills",
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
