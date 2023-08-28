import json
import requests
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django_socketio import events

with open('cricketapi/scrapping/match.json','r') as json_file:
    json_data = json.load(json_file)

def index(request):
    return render(request,'m.html',{'match':json_data})

@events.on_connect
def handle_connect(request,socket,context):
    print("connected to server")
    socket.send(json.dumps(json_data))

@events.on_message(channel="match_updates")
def handle_change_json(request, socket, context, message):
    new_data = message['newData']
    updated = False

    for i, match in enumerate(json_data):
        if any(match[field] == new_data[field] for field in new_data):
            json_data[i] = new_data
            updated = True
            break

    if updated:
        print(json_data)
        socket.send(json.dumps(json_data), channel="match_updates")

def get_json_data(request):
    return JsonResponse(json_data, safe=False)

# @events.on_message(channel="change_json")
# def handle_change_json(request, socket, context, message):
#     new_data = message['newData']
#     updated = False
#
#     for i, match in enumerate(json_data):
#         if match['match_id'] == new_data['match_id'] \
#             or match['status'] == new_data['status'] \
#             or match['details'] == new_data['details'] \
#             or match['team_1_flag'] == new_data['team_1_flag'] \
#             or match['team_2_flag'] == new_data['team_2_flag'] \
#             or match['match_link'] == new_data['match_link'] \
#             or match['match_link_slug'] == new_data['match_link_slug'] \
#             or match['match_scorecard_link'] == new_data['match_scorecard_link'] \
#             or match['team_1_title'] == new_data['team_1_title'] \
#             or match['team_1_run'] == new_data['team_1_run'] \
#             or match['team_2_title'] == new_data['team_2_title'] \
#             or match['team_2_run'] == new_data['team_2_run'] \
#             or match['result'] == new_data['result'] \
#             or match['schedule'] == new_data['schedule']:
#             json_data[i] = new_data
#             updated = True
#             break
#
#     if updated:
#         socket.send(json.dumps(json_data), channel="update")

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

