from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Architecture


def library(request):
    architectures = Architecture.objects.filter(
        is_published=True
    )

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    if search_query:
        architectures = architectures.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    if selected_category:
        architectures = architectures.filter(
            category=selected_category
        )

    categories = (
        Architecture.objects
        .filter(is_published=True)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    context = {
        "architectures": architectures,
        "categories": categories,
        "search_query": search_query,
        "selected_category": selected_category,
        "total_count": Architecture.objects.filter(
            is_published=True
        ).count(),
    }

    return render(
        request,
        "architectures/library.html",
        context
    )


def architecture_detail(request, slug):
    architecture = get_object_or_404(
        Architecture,
        slug=slug,
        is_published=True
    )

    return render(
        request,
        "architectures/detail.html",
        {"architecture": architecture}
    )