from django.contrib import admin

from .models import Room, UserRoom, Message


class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ("code", "code")
    list_filter = ("code", "code")


class UserRoomAdmin(admin.ModelAdmin):
    model = UserRoom
    list_display = ("user", "room")
    list_filter = ("user", "room")


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("user_room", "content")
    list_filter = ("user_room", )


admin.site.register(Room, RoomAdmin)
admin.site.register(UserRoom, UserRoomAdmin)
admin.site.register(Message, MessageAdmin)
