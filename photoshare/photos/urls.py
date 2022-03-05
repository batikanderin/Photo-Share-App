from django.urls import path
from photos import views


urlpatterns = [
    path('',views.gallery, name='gallery'),
    path('view-photo/<str:pk>',views.viewPhoto,name='view-photo'),
    path('add-photo',views.addPhoto,name='add-photo'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutUser,name='logout'),
    path('register',views.registerUser,name='register')
]