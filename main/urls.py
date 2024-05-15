from django.urls import path
from . import views
app_name = "main"

urlpatterns = [
 path("signup/", views.SignupView.as_view(), name="signup"),
 path("login/", views.LoginView.as_view(), name="login"),
 path("", views.HomePageView.as_view(), name="home"),
 path("about/", views.AboutPageView.as_view(), name="about"),
 path("contact/", views.ContactPageView.as_view(), name="contact"),
 path("profile/", views.ProfilePageView.as_view(), name="profile"),
 path("open_chat/", views.OpenChatPageView.as_view(), name="open_chat"),
 path("chat_detail/<uuid:chat_id>/", views.ChatDetailPageView.as_view(), name="chat_detail"),
 path("messages/<uuid:chat_id>/" , views.MessagesPageView.as_view(), name="messages"),
 path("posts/<int:region_id>/", views.PostsPageView.as_view(), name="posts"),
 path("posts_detail/<int:post_id>/", views.PostsDetailPageView.as_view(), name="posts_detail"),
 path("volonter/", views.VolonterPageView.as_view(), name="volonter"),
 path("logout/", views.LogoutView.as_view(), name="logout"),
 path("delete_chat/<uuid:chat_id>/", views.DeleteChatView.as_view(), name="delete_chat"),

]