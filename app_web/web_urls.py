from rest_framework import routers
from app_web import views
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^login_check', views.LoginView.as_view()),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='博客系统API', permission_classes=(), authentication_classes=())),
]
