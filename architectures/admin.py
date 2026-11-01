from django.contrib import admin
from .models import Architecture


@admin.register(Architecture)
class ArchitectureAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "difficulty",
        "created_at",
        "is_published",
    )

    list_filter = (
        "category",
        "difficulty",
        "is_published",
    )

    search_fields = (
        "title",
        "description",
        "category",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


from django.contrib import admin
from .models import WebsiteReview


@admin.register(WebsiteReview)
class WebsiteReviewAdmin(admin.ModelAdmin):

    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'review')
    ordering = ('-created_at',)