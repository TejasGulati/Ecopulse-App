from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Load view
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ai_models.urls')),
    path('api/users/', include('users.urls')),
    path('', index_view, name='index'),
    re_path(r'^(?:.*)/?$', index_view),  # Match all other routes to the React app
]