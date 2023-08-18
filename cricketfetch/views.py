import json
import requests
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


# Create your views here.

def matches(request):
    records = {}
    url = "http://localhost:8000/cricket/all_match_api/"
    response = requests.get(url)
    inshorts_data = response.json()
    records['matches'] = inshorts_data
    return render(request,'matches.html',records)

class MatchDetailsSlug(View):
    def get(self, request, match_link_slug,*args, **kwargs):
        records = {}
        url = f"http://localhost:8000/cricket/match_details{match_link_slug}/"
        response = requests.get(url)
        match_details_data = response.json()
        records['match_details'] = match_details_data
        return render(request,'match_details.html',records)

