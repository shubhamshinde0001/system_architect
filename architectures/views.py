from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Architecture
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages



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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count
from django import forms

from .models import WebsiteReview


class WebsiteReviewForm(forms.ModelForm):

    class Meta:
        model = WebsiteReview
        fields = ['name', 'rating', 'review']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),

            'rating': forms.Select(
                choices=[
                    (5, '★★★★★ - Excellent'),
                    (4, '★★★★ - Very Good'),
                    (3, '★★★ - Good'),
                    (2, '★★ - Average'),
                    (1, '★ - Poor'),
                ],
                attrs={'class': 'form-control'}
            ),

            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your experience...',
                'rows': 5
            }),
        }


def reviews(request):

    if request.method == 'POST':
        form = WebsiteReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you! Your review has been submitted.'
            )
            return redirect('/reviews/')

        messages.error(request, 'Please correct the errors below.')

    else:
        form = WebsiteReviewForm()

    all_reviews = WebsiteReview.objects.all()

    stats = all_reviews.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    context = {
        'form': form,
        'reviews': all_reviews,
        'average_rating': stats['average_rating'] or 0,
        'total_reviews': stats['total_reviews'],
    }

    return render(request, 'architectures/reviews.html', context)

def about(request):
    return render(request, 'architectures/about.html')