# community/forms.py
from django import forms
from .models import Post, Comment, Thread, ThreadReply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "type", "body", "image")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input-light",
                "placeholder": "Título de tu publicación"
            }),
            "type": forms.Select(attrs={
                "class": "input-light",
            }),
            "body": forms.Textarea(attrs={
                "class": "input-light",
                "rows": 8,
                "placeholder": "Escribe tu publicación…"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "file-input-light"
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "input-light",
                "rows": 4,
                "placeholder": "Escribe un comentario…"
            }),
        }

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("forum", "title", "body", "image")
        widgets = {
            "forum": forms.Select(attrs={"class": "input-light"}),
            "title": forms.TextInput(attrs={"class": "input-light", "placeholder": "Título del hilo"}),
            "body": forms.Textarea(attrs={"class": "input-light", "rows": 8, "placeholder": "Contenido del hilo…"}),
            "image": forms.ClearableFileInput(attrs={"class": "file-input-light"}),
        }

class ThreadReplyForm(forms.ModelForm):
    class Meta:
        model = ThreadReply
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": "input-light", "rows": 4, "placeholder": "Tu respuesta…"}),
        }
