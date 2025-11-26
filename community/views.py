from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.apps import apps

from .models import Post, Comment, Forum, Thread, ThreadReply, ModerationLog
from .forms import PostForm, CommentForm, ThreadForm, ThreadReplyForm

# Notification opcional (no rompe si no existe)
try:
    Notification = apps.get_model('accounts', 'Notification')
except LookupError:
    Notification = None

def feed(request):
    qs = Post.objects.filter(is_removed=False).select_related('author')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'community/index.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(is_removed=False).select_related('author')
    form = CommentForm()
    return render(request, 'community/post_detail.html', {
        'post': post, 'comments': comments, 'form': form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # <- IMPORTANTE FILES
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            messages.success(request, 'Publicación creada.')
            return redirect(p.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        owner = post.author
        if request.user.is_superuser:
            if not reason:
                messages.error(request, 'Indica un motivo de moderación.')
                return redirect(post.get_absolute_url())
            post.is_removed = True
            post.save()
            ModerationLog.objects.create(
                content_type='post', object_id=post.id,
                removed_by=request.user, owner=owner, reason=reason
            )
            if Notification:
                Notification.objects.create(
                    user=owner, message=f'Tu publicación "{post.title}" fue retirada: {reason}'
                )
            messages.success(request, 'Publicación retirada.')
        elif request.user == owner:
            post.is_removed = True
            post.save()
            messages.success(request, 'Publicación eliminada por ti.')
        else:
            return HttpResponseForbidden()
        return redirect('community:feed')
    return render(request, 'community/_modal_delete.html', {'obj': post, 'type':'post'})

@login_required
def comment_create(request, slug):
    post = get_object_or_404(Post, slug=slug, is_removed=False)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        c = form.save(commit=False)
        c.post = post
        c.author = request.user
        c.save()
        messages.success(request, 'Comentario publicado.')
    return redirect(post.get_absolute_url())

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        owner = comment.author
        if request.user.is_superuser:
            if not reason:
                messages.error(request, 'Indica un motivo de moderación.')
                return redirect(post.get_absolute_url())
            comment.is_removed = True
            comment.save()
            ModerationLog.objects.create(
                content_type='comment', object_id=comment.id,
                removed_by=request.user, owner=owner, reason=reason
            )
            if Notification:
                Notification.objects.create(
                    user=owner, message=f'Tu comentario fue retirado: {reason}'
                )
            messages.success(request, 'Comentario retirado.')
        elif request.user == owner:
            comment.is_removed = True
            comment.save()
            messages.success(request, 'Comentario eliminado por ti.')
        else:
            return HttpResponseForbidden()
    return redirect(post.get_absolute_url())

# ---------- Foros ----------
def forum_index(request):
    forums = Forum.objects.all().order_by('title')
    return render(request, 'community/forum_index.html', {'forums': forums})

def forum_detail(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    threads = forum.threads.filter(is_removed=False)
    return render(request, 'community/forum_detail.html', {'forum': forum, 'threads': threads})

@login_required
def thread_create(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.save()
            messages.success(request, 'Hilo creado.')
            return redirect(t.get_absolute_url())
    else:
        form = ThreadForm()
    return render(request, 'community/thread_form.html', {'form': form})

def thread_detail(request, forum_slug, slug):
    thread = get_object_or_404(Thread, slug=slug, forum__slug=forum_slug)
    replies = thread.replies.filter(is_removed=False).select_related('author')
    form = ThreadReplyForm()
    return render(request, 'community/thread_detail.html', {'thread': thread, 'replies': replies, 'form': form})

@login_required
def thread_reply(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if thread.is_locked:
        messages.error(request, 'El hilo está cerrado.')
        return redirect(thread.get_absolute_url())
    form = ThreadReplyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        r = form.save(commit=False)
        r.thread = thread
        r.author = request.user
        r.save()
        messages.success(request, 'Respuesta publicada.')
    return redirect(thread.get_absolute_url())

@login_required
def reply_delete(request, pk):
    reply = get_object_or_404(ThreadReply, pk=pk)
    thread = reply.thread
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        owner = reply.author
        if request.user.is_superuser:
            if not reason:
                messages.error(request, 'Indica un motivo de moderación.')
                return redirect(thread.get_absolute_url())
            reply.is_removed = True
            reply.save()
            ModerationLog.objects.create(
                content_type='reply', object_id=reply.id,
                removed_by=request.user, owner=owner, reason=reason
            )
            if Notification:
                Notification.objects.create(
                    user=owner, message=f'Tu respuesta fue retirada: {reason}'
                )
            messages.success(request, 'Respuesta retirada.')
        elif request.user == owner:
            reply.is_removed = True
            reply.save()
            messages.success(request, 'Respuesta eliminada por ti.')
        else:
            return HttpResponseForbidden()
    return redirect(thread.get_absolute_url())

@login_required
def thread_delete(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        owner = thread.author
        if request.user.is_superuser:
            if not reason:
                messages.error(request, 'Indica un motivo de moderación.')
                return redirect(thread.get_absolute_url())
            thread.is_removed = True
            thread.save()
            ModerationLog.objects.create(
                content_type='thread', object_id=thread.id,
                removed_by=request.user, owner=owner, reason=reason
            )
            if Notification:
                Notification.objects.create(
                    user=owner, message=f'Tu hilo "{thread.title}" fue retirado: {reason}'
                )
            messages.success(request, 'Hilo retirado.')
        elif request.user == owner:
            thread.is_removed = True
            thread.save()
            messages.success(request, 'Hilo eliminado por ti.')
        else:
            return HttpResponseForbidden()
        return redirect('community:forum_detail', forum_slug=thread.forum.slug)
    return render(request, 'community/_modal_delete.html', {'obj': thread, 'type':'thread'})
