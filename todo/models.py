from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class OrganizationModel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название организации", unique=True)
    date = models.DateTimeField(auto_now=True)


class ToDoModel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок записи")
    content = models.TextField(verbose_name="Содержание")
    date = models.DateTimeField(auto_now=True)
    create_user = models.ForeignKey(User, null=True, related_name='todos', on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationModel, null=True, related_name='todos', on_delete=models.CASCADE)


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizations = models.ManyToManyField(OrganizationModel, verbose_name="Организации пользователя")
    active_organization = models.ForeignKey(OrganizationModel, null=True, related_name='profile', on_delete=models.SET_NULL)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profilemodel.save()

# Create your models here.
