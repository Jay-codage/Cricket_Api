from django.shortcuts import render
from rest_framework import generics
from .models import CricketMatchDetails
from .serializer import CricketMatchDetailsSerializer
from django.views import generic
from braces.views import SelectRelatedMixin
from django_socketio import events
import json

with open('cricketapi/scrapping/match_details.json','r') as json_file:
    json_data = json.load(json_file)

def index(request):
    return render(request,'match.html',{'match':json_data})

@events.on_connect
def handle_connect(request,socket,context):
    socket.send(json_data)

@events.on_message(channel="change_json")
def handle_change_json(request, socket, context, message):
    new_data = message['newData']
    updated = False

    for i, match in enumerate(json_data):
        if match['match_id'] == new_data['match_id'] \
            or match['status'] == new_data['status'] \
            or match['details'] == new_data['details'] \
            or match['team_1_flag'] == new_data['team_1_flag'] \
            or match['team_2_flag'] == new_data['team_2_flag'] \
            or match['match_link'] == new_data['match_link'] \
            or match['match_link_slug'] == new_data['match_link_slug'] \
            or match['match_scorecard_link'] == new_data['match_scorecard_link'] \
            or match['team_1_title'] == new_data['team_1_title'] \
            or match['team_1_run'] == new_data['team_1_run'] \
            or match['team_2_title'] == new_data['team_2_title'] \
            or match['team_2_run'] == new_data['team_2_run'] \
            or match['result'] == new_data['result'] \
            or match['schedule'] == new_data['schedule']:
            json_data[i] = new_data
            updated = True
            break

    if updated:
        socket.send(json.dumps(json_data), channel="update")

class CricketMatchDetailsCreateView(generics.ListCreateAPIView):
    queryset = CricketMatchDetails.objects.all()
    serializer_class = CricketMatchDetailsSerializer

class MatchDetailsFetch(SelectRelatedMixin,generic.DetailView):
    model = CricketMatchDetails
    select_related = ('cricketdetails','match_rest_api_data')

