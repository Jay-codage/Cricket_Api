from django.shortcuts import render
from rest_framework import generics
from .models import MatchRestApiData
from .serializer import MatchRestApiDataSerializer
from  django.views import generic


class MatchRestApiDataCreateView(generics.ListCreateAPIView):
    queryset = MatchRestApiData.objects.all()
    serializer_class = MatchRestApiDataSerializer

class Listmatch(generic.ListView):
    model = MatchRestApiData

class SingleMatch(generic.DetailView):
    model = MatchRestApiData