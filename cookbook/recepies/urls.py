from django.urls import path
from .views import get_all_recepies, get_user_recepies, create_recepie, cook_recepie, update_recepie
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all_recepies/', get_all_recepies, name='get_all_recepies'),
    path('<str:username>/recepies', get_user_recepies, name='get_user_recepies'),
    # path('<str:username>/recepies/<str:recepie_name>'),
    path('<str:username>/create_recepie', create_recepie, name='create_recepie'),
    path('<str:username>/<int:recepie_id>/cook', cook_recepie, name='cook_recepie'),
    path('<int:recepie_id>/<slug:slug>/update_recepie', update_recepie, name='update_recepie'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                          