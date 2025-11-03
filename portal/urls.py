from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopify_home, name='shopify_home'),
    path('debug/', views.debug_view, name='debug'),
    path("webhook/", views.shopify_webhook, name="shopify_webhook"),
    path("api/whatsapp/webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),

    # path('', views.product_list_view, name='product_list'),
    # path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    # path('create/', views.create_product_with_variants_view, name='create_product'),
    # path('test/', views.test_connection_view, name='test_connection'),
]



