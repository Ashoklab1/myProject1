from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Post, Category, Tag
from .forms import PostForm
from datetime import datetime
from django.contrib.auth.decorators import login_required

def post_list(request):
    query = request.GET.get("q")
    author = request.GET.get("author")
    category = request.GET.get("category")
    tag = request.GET.get("tag")
    sort = request.GET.get("sort", "date")
    tags_selected = request.GET.getlist("tags")
    month = request.GET.get("month")
    year = request.GET.get("year")
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")

    posts = Post.objects.all()

    # Filters
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    if author:
        posts = posts.filter(author__username=author)

    if category:
        posts = posts.filter(category__name=category)

    if tag:
        posts = posts.filter(tags__name=tag)

    if tags_selected:
        posts = posts.filter(tags__name__in=tags_selected).distinct()

    if month and year:
        posts = posts.filter(date__month=month, date__year=year)

    if start_date and end_date:
        posts = posts.filter(date__range=[start_date, end_date])

    # Sorting
    if sort == "title":
        posts = posts.order_by("title")
    else:
        posts = posts.order_by("-date")

    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Month list for dropdown
    months = [
        ("01", "Jan"), ("02", "Feb"), ("03", "Mar"), ("04", "Apr"),
        ("05", "May"), ("06", "Jun"), ("07", "Jul"), ("08", "Aug"),
        ("09", "Sep"), ("10", "Oct"), ("11", "Nov"), ("12", "Dec"),
    ]

    context = {
        "page_obj": page_obj,
        "query": query,
        "sort": sort,
        "category": category,
        "month": month,
        "year": year,
        "months": months,
        "start_date": start_date,
        "end_date": end_date,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "popular_tags": Tag.objects.annotate(post_count=Count('post')).order_by('-post_count')[:10],
        "popular_categories": Category.objects.annotate(post_count=Count('post')).order_by('-post_count')[:10],
        "selected_tags": tags_selected,
    }

    # AJAX request (e.g., Load More or Filters)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("posts/_posts_partial.html", context, request=request)
        next_page = page_obj.next_page_number() if page_obj.has_next() else None
        return JsonResponse({"html": html, "next_page": next_page})

    return render(request, "posts/posts_list.html", context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the tags
            return redirect('posts:post-list')

    else:
        form = PostForm()
    return render(request, 'posts/post_new.html', {'form': form})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})
