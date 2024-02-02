from django import forms
from .models import Category, Husband


# https://docs.djangoproject.com/en/4.2/ref/forms/api/#django.forms.Form
# https://docs.djangoproject.com/en/4.2/ref/forms/fields/
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)
