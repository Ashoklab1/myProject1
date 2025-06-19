from django import forms
from .models import Post, PostImage, Tag, Category
from django.forms.models import inlineformset_factory
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())  # Rich text field
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'banner', 'category', 'tags']

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

# Inline formset for PostImage related to Post
PostImageFormSet = inlineformset_factory(Post, PostImage, form=PostImageForm, extra=3, can_delete=True)
