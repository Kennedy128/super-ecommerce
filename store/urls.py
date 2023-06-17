from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home , name = "home"),
    path('createprofile',views.create_profile,name="create_profile"),
    path('profile/<int:id>',views.profile, name = "profile"),
    path('accounts/profile',views.profile,name='profile'),
    path('profile/edit', views.edit_profile,name = 'edit_profile'),
    path('new/post',views.new_post,name="new_post"),
    

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)