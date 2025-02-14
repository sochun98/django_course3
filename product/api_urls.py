from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.apis import ProductViewSet


router = DefaultRouter()
router.register("", ProductViewSet)

# 127.0.0.1:8000/api/product/
urlpatterns = [
    path("", include(router.urls)),
]