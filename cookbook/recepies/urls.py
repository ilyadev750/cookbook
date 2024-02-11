from django.urls import path
from .views import get_all_recepies, get_user_recepies, create_recepie, delete_recepie, search_recepie_without_product
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all_recepies/', get_all_recepies, name='get_all_recepies'),
    path('<str:username>/recepies/', get_user_recepies, name='get_user_recepies'),
    path('<str:username>/create_recepie/', create_recepie, name='create_recepie'),
    path('<str:username>/delete_recepie/', delete_recepie, name='delete_recepie'),
    path('<str:username>/search_recepie/', search_recepie_without_product, name='delete_recepie'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                          