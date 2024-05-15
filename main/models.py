import uuid
from django.db import models
from django.contrib.auth.models import User

class Regions(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='regions_images/')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    avatar_user = models.ImageField(default='avatar_user.png', upload_to='profile_images/')

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image1 = models.ImageField(upload_to='news_images/')
    image2 = models.ImageField(upload_to='news_images/')
    about_image2 = models.CharField(max_length=200)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.profile.user.username} on {self.news.title}"

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title_status = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} in {self.chat.title}: {self.content}"
 