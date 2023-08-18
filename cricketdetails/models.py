from django.db import models
from django.urls import reverse
from cricketdata.models import MatchRestApiData

class CricketMatchDetails(models.Model):
    match_rest_api_data = models.ForeignKey(MatchRestApiData,on_delete=models.CASCADE,related_name='match_details',default=1)
    match_start = models.CharField(max_length=100,null=True)
    match_about = models.CharField(max_length=200,null=True)
    team_1_name = models.CharField(max_length=50,null=True)
    team_1_score = models.CharField(max_length=50,null=True)
    team_2_name = models.CharField(max_length=50,null=True)
    team_2_score = models.CharField(max_length=50,null=True)
    batting_head = models.JSONField(null=True)
    batsman_name_1 = models.JSONField(null=True)
    batsman_name_2 = models.JSONField(null=True)
    bowling_head = models.JSONField(null=True)
    bowler_names = models.JSONField(null=True)
    reviews = models.CharField(max_length=250,null=True)
    last_30th_balls = models.JSONField(null=True)

    def __str__(self):
        return f"{self.team_1_name} vs {self.team_2_name}"

    def get_absolute_url(self):
        return reverse('cricketdetails:match_details',{'pk':self.pk})

