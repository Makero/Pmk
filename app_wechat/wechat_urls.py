from django.conf.urls import url
from app_wechat import views as wx

urlpatterns = [

    url(r'^validate_token$', wx.validate_token),
    url(r'^msg_handle$', wx.msg_handle),
    url(r'^msg_talk$', wx.msg_talk),
    url(r'^qing_yun_ke$', wx.qing_yun_ke),
    url(r'^music$', wx.music),
    url(r'^music_lrc$', wx.music_lrc),
    url(r'^wx_config$', wx.wx_config),
    url(r'^auth$', wx.user_auth),

]