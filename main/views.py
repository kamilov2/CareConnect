import telebot
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import (
 authenticate, login, 
 logout
)
from .models import (
 Profile, News, Comment, Chat, Message, Regions
)
bot = telebot.TeleBot('7164410880:AAGPToeZ-qpnODonTAT9Sg7bYKdPxKzBf-s')



class SignupView(View):
 def get(self, request):
  if request.user.is_superuser:
   return redirect("main:volonter")
  elif request.user.is_authenticated:
   return redirect("main:home")
  else:
   regions = Regions.objects.all().order_by("id")
   context = {
    "regions":regions
   }
   return render(request, "signup.html", context)
 def post(self, request):
  username = request.POST.get('email')
  print("Username:", username)

  name = request.POST.get('name')
  print("Name:", name)

  surname = request.POST.get('surname')
  print("Surname:", surname)

  age = request.POST.get('age')
  print("Age:", age)

  email = request.POST.get('email')
  print("Email:", email)

  password = request.POST.get('password')
  print("Password:", password)

  confirm_password = request.POST.get('confirm_password')
  print("Confirm Password:", confirm_password)

  region_id = request.POST.get('region')
  print("Region ID:", region_id)

  

  if not username or not email or not password or not confirm_password or not region_id:
      messages.error(request, 'All fields are required.')
  elif password != confirm_password:
      messages.error(request, 'Password and Confirm Password do not match.')
  elif User.objects.filter(username=username).exists():
      messages.error(request, 'Username is already taken.')
  elif User.objects.filter(email=email).exists():
      messages.error(request, 'Email is already registered.')
  else:
      user = User.objects.create_user(username=username, email=email, password=password)
      region = Regions.objects.get(id=region_id)
      profile = Profile(user=user, name=name, surname=surname, age=age, email=email, region=region)
      user.save()
      profile.save()
      login(request, user)
      messages.success(request, 'Registration successful.')
      return redirect('main:login')
  return render(request, 'signup.html')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect("main:home")
        else:    
            return render(request, "login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('main:volonter')
            else:
                return redirect('main:home')  
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "login.html")


class HomePageView(View):
 def get(self, request):
  
  if request.user.is_superuser:
   return redirect('main:volonter')
  if request.user.is_authenticated:
   regions = Regions.objects.all().order_by("id")
   news_banner = News.objects.all().order_by("-created_at")[:4]
   news_popular = News.objects.all().order_by("?")[:4]
   news_list = News.objects.all().order_by("-created_at")[:8]
   profile = Profile.objects.get(user=request.user)
   context = {
    "regions":regions,
    "news_banner":news_banner,
    "news_popular":news_popular,
    "news_list": news_list,
    "profile":profile
   }
   return render(request, "index.html", context)
  else:
   return redirect("main:login")

class AboutPageView(View):
 def get(self, request):
  if request.user.is_authenticated:
   regions = Regions.objects.all().order_by("id")
   profile =  Profile.objects.get(user=request.user)
   context = {
    "regions":regions,
    "profile":profile
   }
   return render(request, "about.html", context)
  elif request.user.is_superuser:
   return redirect('main:volonter')
  else:
   return redirect("main:login")
  
class ContactPageView(View):
 def get(self, request):
  if request.user.is_authenticated:
   regions = Regions.objects.all().order_by("id")
   profile = Profile.objects.get(user=request.user)
   context = {
    "regions":regions,
    "profile":profile
   }
   return render(request, "contact.html", context)
  elif request.user.is_superuser:
   return render(request, "contact.html")
  else:
   return redirect("main:login")
  
 def post(self, request):
   name = request.POST.get('name')
   phone = request.POST.get('phone')
   email = request.POST.get('email')
   message = request.POST.get('message')

   bot.send_message('-1002058115546', f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}")

   return render(request, "contact.html")
 
class ProfilePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            regions = Regions.objects.all().order_by("id")
            profile = Profile.objects.get(user=request.user)
            posts = News.objects.filter(region=profile.region).order_by("-created_at")
            user_chats = Chat.objects.filter(messages__sender=request.user).distinct().order_by("-created_at")

            chats_with_last_message = []
            for chat in user_chats:
                last_message = chat.messages.order_by('-timestamp').first()
                chats_with_last_message.append((chat, last_message))

            context = {
                "regions": regions,
                "profile": profile,
                "chats_with_last_message": chats_with_last_message,
                "posts": posts
            }
            return render(request, "author.html", context)
        elif request.user.is_superuser:
            return render(request, "author.html")
        else:
            return redirect("main:login")

class OpenChatPageView(View):
    def get(self, request):

        if request.user.is_authenticated:
           chat = Chat.objects.create()
           chat.save()
           new_message = Message.objects.create(
                    chat=chat,
                    sender=User.objects.get(username="admin"),
                    content="Assalomu alaykum qanday yordam berishimiz mumkin?",
                )

           new_message.save()

           return redirect("main:chat_detail", chat_id=chat.id)
       

class ChatDetailPageView(View): 
 def get(self, request, chat_id):
   if request.user.is_authenticated:
    regions = Regions.objects.all().order_by("id")
    chat = Chat.objects.get(id=chat_id)
    messages = chat.messages.order_by('timestamp') 
    message_data = []
    for message in messages:
        sender_profile = None
        sender_profile = Profile.objects.filter(user=message.sender).first()
        message_data.append({
            "sender_username": message.sender.username,
            "sender_profile_name": sender_profile.name if sender_profile else None,
            "sender_profile_surname": sender_profile.surname if sender_profile else None,
            "sender_profile_avatar": sender_profile.avatar_user.url if sender_profile else None,
            "content": message.content,
            "timestamp": message.timestamp,
            "read": message.read,
        })
    context = {
        "regions": regions,
        "chat": chat,
        "messages": message_data
    }
    return render(request, "messages.html", context)
   elif request.user.is_superuser:
       return render(request, "messages.html")
   else:
       return redirect("main:login")

class MessagesPageView(View):
   
    def post(self, request, chat_id):
        if request.user.is_authenticated:
            message_content = request.POST.get('message')
            if message_content:
                try:
                    chat = Chat.objects.get(id=chat_id)
                except Chat.DoesNotExist:
                    return redirect("main:profile")

                new_message = Message.objects.create(
                    chat=chat,
                    sender=request.user,
                    content=message_content
                )

                new_message.save()

                return redirect("main:chat_detail", chat_id=chat_id)
            else:
                return redirect("main:home")
        elif request.user.is_superuser:
              try:
                 chat = Chat.objects.get(id=chat_id)
              except Chat.DoesNotExist:
                  return redirect("main:profile")

              new_message = Message.objects.create(
                    chat=chat,
                    sender=request.user,
                    content=message_content
                )

              new_message.save()
          
              
              return redirect("main:chat_detail", chat_id=chat_id)
            
        else:
            return redirect("main:login")
    


class PostsPageView(View):
 def get(self, request, region_id):
  if request.user.is_authenticated:
   regions = Regions.objects.all().order_by("id")
   posts = News.objects.filter(region=region_id).order_by("-created_at")
   news_popular = News.objects.all().order_by("?")[:4]
   profile = Profile.objects.get(user=request.user)

   context = {
    "regions":regions,
    "posts":posts,
    "news_popular":news_popular,
    "profile":profile
   }
   return render(request, "post-list.html", context)
  elif request.user.is_superuser:
   return render(request, "post-list.html")
  else:
   return redirect("main:login")

class PostsDetailPageView(View):
    def get(self, request, post_id):
        if request.user.is_authenticated or request.user.is_superuser:
            regions = Regions.objects.all().order_by("id")
            post = get_object_or_404(News, id=post_id)
            comments = Comment.objects.filter(news=post).order_by('created_at')
            more_news = News.objects.filter(region=post.region).exclude(id=post_id).order_by("-created_at")[:4]
            news_popular = News.objects.all().order_by("?")[:4]
            profile = Profile.objects.get(user=request.user)


            context = {
                "regions": regions,
                "post": post,
                "comments": comments,
                "more_news": more_news,
                "news_popular": news_popular,
                "profile":profile
            }
            return render(request, "post-details.html", context)
        else:
            return redirect("main:login")
    def post(self, request, post_id):
        post = News.objects.get(id=post_id)
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(
                news=post,
                profile=request.user.profile,
                content=content,
            )
            return redirect('main:posts_detail', post_id=post_id)
        
        regions = Regions.objects.all().order_by("id")
        comments = post.comments.all().order_by('created_at')[:35]
        more_news = News.objects.filter(region=post.region).exclude(id=post_id).order_by("-created_at")[:4]
        news_popular = News.objects.all().order_by("?")[:4]
        
        context = {
            "regions": regions,
            "post": post,
            "comments": comments,
            "more_news": more_news,
            "news_popular": news_popular
            
        }
        return render(request, "post-detail.html", context)

class VolonterPageView(View):
    def get(self, request):
        if request.user.is_superuser:
         user_chats = Chat.objects.all()[:35]

         chats_with_last_message = []
         for chat in user_chats:
             last_message = chat.messages.all().order_by('-timestamp').first()
             if last_message:
                 chats_with_last_message.append((chat, last_message))

         context = {
             "chats_with_last_message": chats_with_last_message,
         }

         return render(request, "admin.html", context)  
        else:
           return redirect("main:home")

    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("main:login")
class DeleteChatView(View):
    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        chat.delete()
        return redirect("main:volonter")
