import json
import time
import os
from cricketdata.models import MatchRestApiData

def matchapi(file_path):
    with open(file_path,'r') as json_file:
        data = json.load(json_file)
        MatchRestApiData.objects.all().delete()
        for item in data:
            MatchRestApiData.objects.create(
                match_id=item['match_id'],
                status = item['status'],
                details = item['details'],
                team_1_flag = item['team_1_flag'],
                team_2_flag = item['team_2_flag'],
                match_link = item['match_link'],
                team_1_title = item['team_1_title'],
                team_2_title = item['team_2_title'],
                team_1_run = item.get('team_1_run',''),
                team_2_run = item.get('team_2_run',''),
                result = item.get('result',''),
                schedule = item['schedule'],
            )

def monitor_file_changes(file_path):
    last_modified_time = os.stat(file_path).st_mtime
    while True:
        time.sleep(1)
        current_modified_time = os.stat(file_path).st_mtime
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            print('Updating the database...')
            matchapi(file_path)

if __name__ == '__main__':
    json_file_path = 'cricketapi\scrapping\match.json'
    monitor_file_changes(json_file_path)