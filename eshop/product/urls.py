from rest_framework.urls import urlpatterns
from django.urls import path
from .views import get_product, get_products, upload_product_image, Radhas, radha
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("products/", view=get_products, name="Products"),
    path(
        route="product/upload_images", view=upload_product_image, name="upload_images"
    ),
    path("product/<str:pk>/", view=get_product, name="get_product_details"),
    path(route="radha/", view=Radhas, name="Radhas"),
    path("items/<str:name>/", view=radha, name="radha"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
