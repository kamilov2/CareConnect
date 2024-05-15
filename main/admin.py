from django.contrib import admin
from .models import Regions, Profile, News, Comment, Chat, Message

class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'surname', 'age', 'email', 'region')
    search_fields = ('name', 'surname', 'email', 'region__name')
    list_filter = ('region',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'region', 'created_at')
    search_fields = ('title', 'content', 'region__name')
    list_filter = ('region', 'created_at')
    readonly_fields = ('created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'profile', 'content', 'created_at')
    search_fields = ('news__title', 'profile__user__username', 'content')
    list_filter = ('created_at', 'news')

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'closed')
    search_fields = ('title',)
    list_filter = ('created_at', 'closed')
    readonly_fields = ('id', 'created_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content', 'timestamp', 'read')
    search_fields = ('chat__title', 'sender__username', 'content')
    list_filter = ('timestamp', 'read')

admin.site.register(Regions, RegionsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
 