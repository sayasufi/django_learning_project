from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class WomenHome(ListView):
    # model = Women
    template_name = "women/index.html"
    context_object_name = "posts"

    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "cat_selected": 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related("cat")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["title"] = "Главная страница"
    #     context["menu"] = menu
    #     context["posts"] = Women.published.all().select_related("cat")
    #     context["cat_selected"] = int(self.request.GET.get("cat_id", 0))
    #     return context


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #            handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()

    return render(
        request,
        "women/about.html",
        {"title": "О сайте", "menu": menu, "form": form},
    )


class ShowPost(DetailView):
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"]
        context["menu"] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(FormView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")

    extra_context = {
        "menu": menu,
        "title": "Добавление статьи",
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Категория - " + cat.name
        context["menu"] = menu
        context["cat_selected"] = cat.id
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related(
            "cat"
        )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = "Тег: " + tag.tag
        context["menu"] = menu
        context["cat_selected"] = None
        return context

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")
