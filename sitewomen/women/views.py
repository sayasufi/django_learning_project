import uuid

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": Women.published.all().select_related("cat"),
        "cat_selected": 0,
    }

    return render(request, "women/index.html", context=data)


def handle_uploaded_file(f):
    name = f.name
    ext = ""

    if "." in name:
        ext = name[name.rindex(".") :]
        name = name[: name.rindex(".")]

    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data["file"])
    else:
        form = UploadFileForm()

    return render(
        request,
        "women/about.html",
        {"title": "О сайте", "menu": menu, "form": form},
    )


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }

    return render(request, "women/post.html", context=data)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()

    return render(
        request,
        "women/addpage.html",
        {"menu": menu, "title": "Добавление статьи", "form": form},
    )


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(
        is_published=Women.Status.PUBLISHED
    ).select_related("cat")

    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }

    return render(request, "women/index.html", context=data)
