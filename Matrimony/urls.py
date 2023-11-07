"""
URL configuration for Matrimony project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static 
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('',user_views.home,name='home'),
    path('landing',user_views.landing,name='landing'),
    path('about/',user_views.about,name = 'about'),
    
    path('profile/<int:id>/',user_views.profile,name='profile'),
    path('unbookmark/<int:item_id>/',user_views.unbookmark,name='unbookmark'),
    path('add_to_bookmarks/<int:id>/',user_views.add_to_bookmarks,name='add_to_bookmarks'),
    path('bookmarks/',user_views.bookmarks,name='bookmarks'),
    path('accept_friend_request/<int:request_id>/',user_views.accept_friend_request,name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/',user_views.decline_friend_request,name='decline_friend_request'),
    path('send_friend_request/<int:to_user_id>/',user_views.send_friend_request,name='send_friend_request'),
    path('received_requests/',user_views.received_requests,name='received_requests'),
    path('sent_requests/',user_views.sent_requests,name='sent_requests'),
    path('accepted_requests/',user_views.accepted_requests,name='accepted_requests'),
    
    path('updateform1',user_views.updateform1,name='updateform1'),
    path('updateform2',user_views.updateform2,name='updateform2'),
    path('updateform3',user_views.updateform3,name='updateform3'),
    path('createform1',user_views.createform1,name='createform1'),
    path('createform2',user_views.createform2,name='createform2'),
    path('createform3',user_views.createform3,name='createform3'),
    path('createform4',user_views.createform4,name='createform4'),
    path('updatepreferences',user_views.updatepreferences,name='updatepreferences'),
   
    
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


