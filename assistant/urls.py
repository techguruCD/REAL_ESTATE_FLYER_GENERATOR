# here we are import path from in-built django-urls
from django.urls import path
# here we are importing all the Views from the views.py file
from . import views
from real_estate_flyer_generator import settings
from django.conf.urls.static import static

# a list of all the urls
urlpatterns = [
    path('', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('generate/', views.generate, name='generate'),
    path('error-handler/', views.error_handler, name='error_handler'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)