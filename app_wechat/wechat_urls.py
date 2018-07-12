from django.conf.urls import url
from app_wechat import views

urlpatterns = [
    url(r'^validate_token$', views.validate_token),
    url(r'^msg_handle$', views.msg_handle),
    url(r'^msg_talk$', views.msg_talk),
    url(r'^qing_yun_ke$', views.qing_yun_ke),
    url(r'^music$', views.music),
    url(r'^music_lrc$', views.music_lrc),
    url(r'^wx_config$', views.wx_config),
    url(r'^auth', views.UserAuthView.as_view()),
]
