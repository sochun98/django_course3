from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.views import RandomNumberTemplateView, RandomNumberView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("todo/", include("todo.urls")),
    path("random/template/", RandomNumberTemplateView.as_view()),
    path("random/view/", RandomNumberView.as_view()),
]

# if settings.DEBUG:
    # urlpatterns += static(settings.FILE_URL, document_root=settings.FILE_ROOT)