# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Citizen

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_citizen_on_user_create(sender, instance, created, **kwargs):
#     if created:
#         Citizen.objects.create(user=instance, full_name=instance.get_full_name() or instance.username)
