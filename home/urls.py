from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('details/<int:pkId>', views.Details, name="details"),
    path('<str:categoryname>',views.categoryProduct, name="category"),
    path('sell/', views.sell, name="sell"),
    path('account/<str:username>', views.account, name='account'),
    path('account/edit/<str:username>', views.editProfile, name="edit_profile"),
    path('delpost/', views.delProfile, name="delpost"),
    path('delads/<int:pkId>',views.delAds, name="delads"),
    path('follow/<str:username>', views.follow, name="follow"),
]