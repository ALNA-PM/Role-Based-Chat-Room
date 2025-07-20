
from django.contrib import admin
from .models import Role, User, Message

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'permissions')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')
    list_filter = ('visible_to_roles',)

admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
