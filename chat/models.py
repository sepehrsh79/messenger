from django.core.validators import RegexValidator
from django.db import models

from django.db import models

from account.models import BaseFieldsModel


class Room(BaseFieldsModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=8, unique=True)
    is_active = models.BooleanField(default=False)

    def members(self):
        return UserRoom.objects.filter(room_id=self.id)

    class Meta:
        ordering = ('create_date',)

    def __str__(self):
        return self.code


class UserRoom(BaseFieldsModel):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='user_user_room',
                             verbose_name='کاربر')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='room_user_room',
                             verbose_name='اتاق')

    class Meta:
        ordering = ('create_date',)

    def __str__(self):
        return f'{self.user} , {self.room}'


class Message(BaseFieldsModel):
    user_room = models.ForeignKey('UserRoom', on_delete=models.CASCADE, related_name='user_room_message',
                                 verbose_name='اتاق کاربر')
    content = models.TextField()

    class Meta:
        ordering = ('create_date',)

    def __str__(self):
        return f'{self.user_room}'
