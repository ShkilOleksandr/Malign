"""
URL configuration for Malign project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from blog.views import update_user_info, update_creator_info, visit_user, visit_creator

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('', views.nothing,name="nothing" ),
    path('home/', views.home,name="home" ),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('creator_signup/', views.creator_signup, name='creator_signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('upload_podcast/', views.upload_podcast, name='upload_podcast'),
    path('podcast/<int:podcast_id>/', views.podcast_detail, name='podcast_detail'),
    path('podcast/<int:podcast_id>/comment/', views.add_comment, name='add_comment'),
    path('user/update/', update_user_info, name='update_user_info'),
    path('creator/update/', update_creator_info, name='update_creator_info'),
    path('visiting_user/<int:user_id>/',visit_user, name='visit_user'),
    path('visiting_creator/<int:user_id>/',visit_creator, name='visit_creator'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)