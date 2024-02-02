from django.urls import path
from .views import login_user, register_user, logout

urlpatterns = [
    path('login/', login_user, name='login'),
    path('registration/', register_user, name='registration'),
    path('logout/', logout, name='logout'),
]   