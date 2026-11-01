
from django.db import models
from django.utils.text import slugify


class Architecture(models.Model):

    CATEGORY_CHOICES = [
        ("Distributed Systems", "Distributed Systems"),
        ("E-Commerce", "E-Commerce"),
        ("Social Media", "Social Media"),
        ("Streaming Services", "Streaming Services"),
        ("Transportation", "Transportation"),
        ("AI / ML Systems", "AI / ML Systems"),
        ("Database Systems", "Database Systems"),
        ("Other", "Other"),
    ]

    DIFFICULTY_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    difficulty = models.CharField(
        max_length=30,
        choices=DIFFICULTY_CHOICES,
        default="Beginner"
    )

    html_file = models.FileField(
        upload_to="architecture_guides/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_published = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class WebsiteReview(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}/5"