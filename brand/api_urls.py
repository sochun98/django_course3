from django.urls import path, include
from rest_framework.routers import DefaultRouter
from brand.apis import BrandViewSet

router = DefaultRouter()
router.register("", BrandViewSet)

# 127.0.0.1:8000/api/brand/
urlpatterns = [
    path("", include(router.urls)),
]