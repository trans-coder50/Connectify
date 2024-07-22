from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path as url
from django.views.static import serve
urlpatterns=[

    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

  url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/', views.logoutUser , name = "logout"),   
    path('messages/', views.messages , name = "messages"),
    path('notification/', views.notification , name = "notification"),
    path('invitation/', views.invitation , name = "invitation"),
    path('saves/', views.saves , name = "saves"),
    path('profile/', views.profile , name = "profile"),
    path('search/', views.search , name = "search"),
    path('my_view/' , views.my_view , name = "my_view"),
    path('save_post/' , views.save_post , name = "save_post"),
    path('heart_post/' , views.heart_post , name = "heart_post"),
    path('stat/' , views.stat , name = "stat"),
    path('userStaff/' , views.userStaff , name = "userStaff"),
    path('createInvitation/' , views.createInvitation , name = "createInvitation"),
    path('createFriends/' , views.createFriends , name = "createFriends"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
