# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def avatar_upload_to(instance, filename):
    return f'accounts/avatars/{instance.user_id}/{filename}'
def upload_avatar(instance, filename):
    return avatar_upload_to(instance, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Campos de personalización
    display_name    = models.CharField(max_length=120, blank=True, default='')
    gamer_tag       = models.CharField(max_length=60, blank=True, default='')
    bio             = models.TextField(blank=True, default='')
    country         = models.CharField(max_length=60, blank=True, default='')
    city            = models.CharField(max_length=60, blank=True, default='')
    favorite_domain = models.CharField(
        max_length=20,
        choices=(
            ('tiempo',  'Tiempo'),
            ('niebla',  'Niebla'),
            ('cenizas', 'Cenizas'),
            ('vientos', 'Vientos'),
            ('piedra',  'Piedra'),
        ),
        blank=True,
        default=''
    )
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)

    def __str__(self):
        return self.display_name or self.user.username

class Notification(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Notif({self.user.username}): {self.message[:32]}'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Al crear un User, crea Profile automáticamente.
    # Si ya existe el User, asegúrate de que el Profile exista.
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
