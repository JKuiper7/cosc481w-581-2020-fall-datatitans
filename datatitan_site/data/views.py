# The "view" in django mvc architecture which integrates with html to display data

from django.shortcuts import render
from django.utils import timezone
from data.models import Country, CovidDataClean
from blog.models import Post, Comment
from data.scripts.generate_graphs import gen_graph
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_GET
from data.forms import ChartSelector, CommentForm
from django.views.decorators.cache import cache_page


@require_GET
@cache_page(60 * 10)
def home(request):
    # Get items from the form
    form = ChartSelector(request.GET)
    if form.is_valid():
        countries = form.cleaned_data["iso_code"].values_list("iso_code", flat=True)
        data_category = form.cleaned_data["data_type"]
        chart_type = form.cleaned_data["chart_type"]
        metric = form.cleaned_data["metric"]
    else:
        countries = []
        data_category = "TOTAL_CASES"
        chart_type = "LINE"
        metric = "raw"
    countries = list(dict.fromkeys(countries))
    countries = [country for country in countries if country != "none"]
    countries = list(filter(None, countries))
    table_fields = (
        "location",
        "population",
        "total_cases",
        "total_deaths",
        "total_tests",
        "total_cases_per_million",
        "total_deaths_per_million",
        "total_tests_per_thousand",
    )
    country_stats = (
        CovidDataClean.objects.order_by("iso_code", "-date")
        .distinct("iso_code")
        .filter(iso_code__in=countries)
        .values_list(*table_fields)
    )
    return render(
        request,
        "data.html",
        {
            "chart": gen_graph(*countries, category=str.lower(data_category), chart_type=chart_type, metric=metric),
            "country_selector": form.as_p(),
            "fields": (field.replace("_", " ").title() for field in table_fields),
            "country_table": country_stats,
        }
        if form.is_valid()
        else {
            "chart": "",
            "country_selector": ChartSelector().as_p(),
            "fields": table_fields,
            "country_table": None,
        },
    )


def about(request):
    return render(request, "about.html", {})


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog.html", {"posts": posts})


def blog_detail(request, blog_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.username
            comment.text = request.text
            comment.created_date = timezone.now()
            comment.blog_id = blog_id
            comment.save()
    blog_post = Post.objects.get(pk=blog_id)
    comments = Comment.objects.get(blog_id=blog_id)
    commentForm = CommentForm()

    return render(
        request,
        "blog_detail.html",
        {"post": blog_post, "comments": comments, "form": CommentForm},
    )
