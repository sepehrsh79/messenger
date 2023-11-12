from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


def avatar_image_dir_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return f'brand/{filename}'


class BaseFieldsModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey('account.CustomUser', on_delete=models.DO_NOTHING, related_name='created_%(class)ss',
                                   null=True, blank=True)
    updated_by = models.ForeignKey('account.CustomUser', on_delete=models.DO_NOTHING, related_name='updated_%(class)ss',
                                   null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['create_date']

    def is_updated_after_crate(self):
        return (self.update_date - self.create_date).seconds > 2

    def save(self, *args, **kwargs):
        self.posted_user = kwargs.pop('user', None)
        if self.posted_user and not self.posted_user.is_anonymous:
            if self.pk is None:
                self.created_by = self.posted_user
            self.updated_by = self.posted_user
        super(BaseFieldsModel, self).save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, BaseFieldsModel, PermissionsMixin):
    username = models.CharField(max_length=11, validators=[RegexValidator(r'^[0-9]{11}$')], unique=True,
                                help_text='example: 09121328462')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_image_dir_path, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @staticmethod
    def is_staff(self):
        return self.is_superuser
