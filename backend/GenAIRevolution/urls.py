from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ai_models.urls')),
    path('api/users/', include('users.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!api/)(?!admin/)(?!static/).+', TemplateView.as_view(template_name='index.html')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)