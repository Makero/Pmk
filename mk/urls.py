"""mk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler404
from django.contrib import admin
from wechat import views as wx
from blog import views as bg


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/validate_token', wx.validate_token),
    url(r'^api/msg_handle', wx.msg_handle),
    url(r'^api/msg_talk', wx.msg_talk),
    url(r'^api/qing_yun_ke', wx.qing_yun_ke),
    url(r'^api/music', wx.music),
    url(r'^api/wx_config', wx.wx_config),

    url(r'^api/blog/info', bg.info),
]

handler404 = wx.page_not_found
