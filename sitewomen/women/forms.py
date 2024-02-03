from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


# https://docs.djangoproject.com/en/4.2/ref/forms/api/#django.forms.Form
# https://docs.djangoproject.com/en/4.2/ref/forms/fields/


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = (
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    )
    code = "russian"

    def __init__(self, message=None):
        self.message = (
            message
            if message
            else "Должны присутствовать только русские символы, дефис и пробел."
        )

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    def clean_title(self):
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError(
                "Должны присутствовать только русские символы, дефис и пробел."
            )
        return title

    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категории",
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False,
        empty_label="Не замужем",
        label="Муж",
    )

    class Meta:
        model = Women
        fields = [
            "title",
            "slug",
            "content",
            "photo",
            "is_published",
            "cat",
            "husband",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")
