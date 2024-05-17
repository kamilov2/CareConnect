# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import News, Profile
# from django.core.mail import send_mail

# @receiver(post_save, sender=News)
# def notify_profiles_on_news_creation(sender, instance, created, **kwargs):
#     if created:
#         profiles = Profile.objects.all()
#         subject = f'News: {instance.title}'
#         message = f'News in site visit news: "{instance.title}".\n\n{instance.content} https://careconnect.uz/posts_detail/{instance.id}'
#         recipient_list = [profile.email for profile in profiles]
        
#         print(recipient_list)
        
#         send_mail(
#             subject,
#             message,
#             'ivpplatform@yandex.com',  
#             recipient_list,
#             fail_silently=False,
#         )
