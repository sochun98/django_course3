from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.views import RandomNumberTemplateView, RandomNumberView


# 127.0.0.1:8000/
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("users.api_urls")),
    path('api/blog/', include("blog.api_urls")),
    path("api/product/", include("product.api_urls")),
    path("api/brand/", include("brand.api_urls")),
    path("api/todo/", include("todo.api_urls")),
    path("todo/", include("todo.urls")),
    path("random/template/", RandomNumberTemplateView.as_view()),
    path("random/view/", RandomNumberView.as_view()),
    # 127.0.0.1:8000/api-auth/login/
    # 127.0.0.1:8000/api-auth/logout/ -> session flush cookie
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# if settings.DEBUG:
    # urlpatterns += static(settings.FILE_URL, document_root=settings.FILE_ROOT)