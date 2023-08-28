from django.urls import path,re_path
from cricketfetch import views
# from django_socketio import views as socketio_views

app_name ='cricketfetch'

urlpatterns = [
    path('',views.matches,name="matches"),
    path('match_details<slug:match_link_slug>/',views.MatchDetailsSlug.as_view(),name='match-details'),
    path('socket.io/',views.index,name='match'),
    path('socket.io/get_json_data/', views.get_json_data, name='get_json_data'),
    # re_path(r'^socket\.io', socketio_views.socketio, name="socketio"),
    # re_path(r'^socket\.io/(?P<channel_name>\w+)/$', socketio_views.socketio, name="socketio"),
]