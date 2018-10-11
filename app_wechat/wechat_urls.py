from django.conf.urls import url
from app_wechat import views

urlpatterns = [
    url(r'^validate_token', views.ValidateTokenView.as_view()),
    url(r'^msg_handle', views.MsgHandleView.as_view()),
    url(r'^msg_talk', views.ZyouRobotView.as_view()),
    url(r'^qing_yun_ke', views.QYKView.as_view()),
    url(r'^music_url', views.MusicView.as_view()),
    url(r'^music_lrc', views.MusicLRCView.as_view()),
    url(r'^wx_config', views.WxConfigView.as_view()),
    url(r'^auth', views.UserAuthView.as_view()),
    url(r'^save_image', views.SaveImage.as_view()),
]
