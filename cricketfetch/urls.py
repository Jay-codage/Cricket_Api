from django.urls import path
from cricketfetch import views

app_name ='cricketfetch'

urlpatterns = [
    path('',views.matches,name="matches"),
    path('match_details<slug:match_link_slug>/',views.MatchDetailsSlug.as_view(),name='match-details')
]