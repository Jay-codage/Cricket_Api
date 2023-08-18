from django.urls import path
from cricketdetails import views

app_name = 'cricketdetails'

urlpatterns = [
    path('match_details',views.CricketMatchDetailsCreateView.as_view(),name='match_details'),
]