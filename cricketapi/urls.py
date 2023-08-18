from django.urls import path
from cricketapi import views

app_name = 'cricketapi'

urlpatterns = [
    path('all_match_api/',views.CricketApi.as_view(),name='all-match'),
    path('all_match_api/match_details/',views.Match_details_api.as_view(),name='match_details'),
    path('all_match_api/scorecard/',views.Match_Scorecard_api.as_view(),name='match_scorecard'),
    path('match_details<slug:match_link_slug>/',views.MatchDetailsSlug.as_view(),name = 'match-details'),
    path('match_scorecard<slug:match_scorecard_link_slug>/',views.MatchScorecardSlug.as_view(),name='match-scorecard'),
]