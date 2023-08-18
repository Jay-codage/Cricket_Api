from django.urls import path
from cricketdata import views

app_name = 'cricketdata'

urlpatterns = [
    path('matches/',views.MatchRestApiDataCreateView.as_view(),name='all_matches'),
    path('all_matches/',views.Listmatch.as_view(),name='list_match'),
    path('all_matches/in/<slug>/',views.SingleMatch.as_view(),name = 'single'),

]