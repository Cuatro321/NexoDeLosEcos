# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileForm
from .models import Notification

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # perfil propio o de otro usuario ?user=username
        username = self.request.GET.get('user')
        u = get_object_or_404(User, username=username) if username else self.request.user
        ctx['u'] = u
        ctx['profile'] = getattr(u, 'profile', None)
        # últimas 10 notificaciones
        ctx['notifications'] = Notification.objects.filter(user=u).order_by('-created')[:10]
        # contador de no leídas (para el template)
        ctx['unread_count'] = Notification.objects.filter(user=u, is_read=False).count()
        return ctx

@login_required
def profile_edit(request):
    p = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=p)
    return render(request, 'accounts/profile_edit.html', {'form': form})

def register_view(request):
    """Registro como vista de función (no clase)."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)
            messages.success(request, 'Cuenta creada. ¡Bienvenido al Nexo!')
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def notifications_list(request):
    items = Notification.objects.filter(user=request.user).order_by('-created')
    # marca como leídas al entrar
    items.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'items': items})
