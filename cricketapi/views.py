import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import generic

class CricketApi(APIView):
    def get(self,request):
        with open('cricketapi/scrapping/match.json') as jsonfile:
            data = json.load(jsonfile)
            return Response(data)

class Match_details_api(APIView):
    def get(self,request):
        with open('cricketapi/scrapping/match_details.json') as jsonfile:
            data = json.load(jsonfile)
            return Response(data)

class Match_Scorecard_api(APIView):
    def get(self,request):
        with open('cricketapi/scrapping/scorecard.json') as jsonfile:
            data = json.load(jsonfile)
            return Response(data)

class MatchDetailsSlug(APIView):
    def get(self, request, match_link_slug):
        with open("cricketapi/scrapping/match_details.json", 'r') as jsonfile:
            data = json.load(jsonfile)
            match_detail = next((match for match in data if match['match_link_slug'] == match_link_slug), None)
            if match_detail:
                return Response(match_detail)
            else:
                return Response({"message": "Match not found."}, status=404)

class MatchScorecardSlug(APIView):
    def get(self, request, match_scorecard_link_slug):
        with open("cricketapi/scrapping/scorecard.json", 'r') as jsonfile:
            data = json.load(jsonfile)
            match_detail = next((match for match in data if match['match_scorecard_link_slug'] == match_scorecard_link_slug), None)
            if match_detail:
                return Response(match_detail)
            else:
                return Response({"message": "Match not found."}, status=404)


