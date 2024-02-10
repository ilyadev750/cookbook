from django.urls import path
from .views import get_recepie_products, add_product_to_recipe, delete_product_from_recepie, cook_recepie
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<str:username>/<slug:recepie_slug>/', get_recepie_products, name='get_recepie_products'),
    path('<str:username>/<slug:recepie_slug>/add_product/', add_product_to_recipe, name='add_product_to_recipe'),
    path('<str:username>/<slug:recepie_slug>/delete_product/', delete_product_from_recepie, name='delete_product_from_recepie'),
    path('<str:username>/<slug:recepie_slug>/cook/', cook_recepie, name='cook_recepie'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                          