import notifications
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from AlertManagement import settings

admin.autodiscover()
dajaxice_autodiscover()
urlpatterns = [
    url(r'^', include('Registrations.urls', namespace='Registrations', app_name='Registrations')),
    url(r'^profile/', include('Profiles.urls', namespace='Profiles', app_name='Profiles')),
    url(r'^alert/', include('Alerts.urls', namespace='Alerts', app_name='Alerts')),
    url(r'^groups/', include('Groups.urls', namespace='Groups', app_name='Groups')),
    url(r'^api/', include('API.urls', namespace='API', app_name='API')),
    url(r'^admin/', include(admin.site.urls)),
    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
