from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def add_user_to_member_group(sender, instance, created, **kwargs):
    if created:
        member_group, _ = Group.objects.get_or_create(name='member')
        instance.groups.add(member_group)
        instance.role = User.MEMBER
        instance.save()
