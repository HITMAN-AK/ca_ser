from django.urls import path,re_path
from .views import Log,Signup,Cuname,Users,FetchMessages,StoreMessages
from .consumers import ChatConsumer

urlpatterns = [
    path('log/',Log.as_view(),name="log-in" ),
    path('signup/',Signup.as_view(),name="sign-up" ),
    path('cu/',Cuname.as_view(),name="check-username"),
    path('users/',Users.as_view(),name="users"),
    path('sm/', FetchMessages.as_view(), name='fetch_messages'),
    path('offmess/', StoreMessages.as_view(), name='offline-messages'),

]