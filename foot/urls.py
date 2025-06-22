from django.urls import path
from . import views

# making the routes to visit those pages

urlpatterns = [
   
    # after this visit the project(voyage) urls.py
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    

    path('', views.Home, name="home" ),
    path('room/<str:pk>/', views.room, name="room"),  
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),  



    path('create-room/', views.createRoom, name="create-room"),
    # THEN GO TO HOME.HTML TO CREATE A LINK (createroom).
    # path to update the form
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    # delete url path for feed/participants on the home page
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    # go to nav and update the settings link

    
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
  
]