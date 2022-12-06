from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from TaskManager import settings
from TaskManager.accounts.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home page'),
    path('accounts/', include('TaskManager.accounts.urls')),
    path('tasks/', include('TaskManager.tasks.urls')),
    path('vacations/', include('TaskManager.vacations.urls')),
    # TODO: Fix this 'common' path
    # probably needed later
    # path('common/', include('TaskManager.common.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
