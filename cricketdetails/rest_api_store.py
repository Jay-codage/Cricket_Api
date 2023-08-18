import json
import time
import os
from cricketdetails.models import CricketMatchDetails
from cricketdata.models import MatchRestApiData

def store_from_json(file_path):
    with open(file_path,'r') as json_file:
        data = json.load(json_file)
        CricketMatchDetails.objects.all().delete()
        for item in data:

            CricketMatchDetails.objects.create(
                match_start = item.get('match_start',''),
                match_about = item.get('match_about'),
                team_1_name = item.get('team_1_name'),
                team_1_score = item.get('team_1_score'),
                team_2_name = item.get('team_2_name'),
                team_2_score = item.get('team_2_score'),
                batting_head = item.get('batting_head'),
                batsman_name_1 = item.get('batsman_name_1'),
                batsman_name_2 = item.get('batsman_name_2'),
                bowling_head = item.get('bowling_head'),
                bowler_names = item.get('bowler_names'),
                reviews = item.get('reviews'),
                last_30th_balls = item.get('last_30th_balls'),
            )

def monitor_file_changes(file_path):
    last_modified_time = os.stat(file_path).st_mtime
    while True:
        time.sleep(1)
        current_modified_time = os.stat(file_path).st_mtime
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            print('Updating the database...')
            store_from_json(file_path)

if __name__ == '__main__':
    json_file_path = 'cricketapi\scrapping\match_details.json'
    monitor_file_changes(json_file_path)