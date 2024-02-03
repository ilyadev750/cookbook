from django.urls import path
from .views import login_user, register_user, logout_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_user, name='login'),
    path('registration/', register_user, name='registration'),
    path('logout/', logout_user, name='logout'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                          