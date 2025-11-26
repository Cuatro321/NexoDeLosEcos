
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import time

def upload_post_image(instance, filename):
    return f'community/posts/{instance.author_id}/{int(time.time())}_{filename}'

def upload_forum_image(instance, filename):
    return f'community/forums/{instance.author_id}/{int(time.time())}_{filename}'

class Post(models.Model):
    POST_TYPES = (
        ('post', 'Publicación'),
        ('review', 'Reseña'),
    )
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title    = models.CharField(max_length=140)
    body     = models.TextField()
    type     = models.CharField(max_length=10, choices=POST_TYPES, default='post')
    image    = models.ImageField(upload_to=upload_post_image, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    slug     = models.SlugField(max_length=180, unique=True, blank=True)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.author_id}-{int(time.time())}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('community:post_detail', args=[self.slug])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post     = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body     = models.TextField(max_length=1000)
    created  = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comentario de {self.author}'

class Forum(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug        = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('community:forum_detail', args=[self.slug])

class Thread(models.Model):
    forum    = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    title    = models.CharField(max_length=150)
    body     = models.TextField()
    image    = models.ImageField(upload_to=upload_forum_image, blank=True, null=True)
    slug     = models.SlugField(max_length=180, unique=True, blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.forum_id}-{self.author_id}-{int(time.time())}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('community:thread_detail', args=[self.forum.slug, self.slug])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class ThreadReply(models.Model):
    thread   = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_replies')
    body     = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Respuesta de {self.author}'

class ModerationLog(models.Model):
    CONTENT_TYPES = (('post','Post'), ('comment','Comment'), ('thread','Thread'), ('reply','Reply'))
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    object_id    = models.PositiveIntegerField()
    removed_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mod_actions')
    owner        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mod_owners')
    reason       = models.TextField()
    created      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.content_type} #{self.object_id} – {self.removed_by}'
