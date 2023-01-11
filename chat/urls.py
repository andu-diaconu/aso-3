from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='sign up'),
    path('login/', views.signin, name='sign in'),
    path('logout/', views.signout, name='sign out'),
    path('', views.general, name='root'),
    path('search_room', views.search_room, name='search_room'),
    path('<str:channel>/', views.room, name='room'),
    path('create-page', views.create_room, name='create form'),
    path('create-room', views.create, name='create req'),
    path('send_message', views.send_message, name='send message'),
    path('getMessages/<str:room>', views.get_messages, name="fetch messages")
]