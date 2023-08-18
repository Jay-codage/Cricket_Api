from django.shortcuts import render
from rest_framework import generics
from .models import CricketMatchDetails
from .serializer import CricketMatchDetailsSerializer
from django.views import generic
from braces.views import SelectRelatedMixin

class CricketMatchDetailsCreateView(generics.ListCreateAPIView):
    queryset = CricketMatchDetails.objects.all()
    serializer_class = CricketMatchDetailsSerializer

class MatchDetailsFetch(SelectRelatedMixin,generic.DetailView):
    model = CricketMatchDetails
    select_related = ('cricketdetails','match_rest_api_data')

