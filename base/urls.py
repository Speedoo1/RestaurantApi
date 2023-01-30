from django.urls import path

from base import views

urlpatterns = [
    path('', views.home),
    path('singlefood/<str:pk>/', views.singlefood),
    path('login/', views.logins),
    path('like/<str:pk>/', views.like),
    path('favourite/', views.itemlikedbyuser),
    path('signup/', views.crateAccount),
    path('logout/', views.logouts)
]
