import socket
import time
import requests
from bs4 import BeautifulSoup
import json
import sched


def cricket_api(hostname):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((hostname, 80))
        print("Connected to", hostname)

        out = []

        request = "GET / HTTP/1.1\r\nHost: " + hostname + "\r\n\r\n"
        client_socket.sendall(request.encode())

        response = client_socket.recv(4096)
        response_text = response.decode()

        location_header = response_text.split('Location: ')[1].split('\r\n')[0]
        print("Location:", location_header)

        req = requests.get(f"{location_header}")
        soup = BeautifulSoup(req.content, 'html.parser')

        for single_match in soup.find_all('div',class_='ds-p-2 ds-bg-fill-hsb-scorecell ds-text-compact-2xs ds-rounded-xl ds-h-[146px]'):
            match_start = single_match.find('span', class_='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5')
            match_id = single_match.find('span', class_='ds-text-tight-xs ds-text-typo-mid2')
            match_result = single_match.find('p', class_='ds-text-tight-xs ds-truncate ds-text-typo')
            match_schedule = single_match.find('div',class_='ds-flex ds-mt-2 ds-pt-1.5 ds-border-t ds-border-line-default-translucent')
            match_link = single_match.find('a',class_='ds-no-tap-higlight')

            team_1_flag = single_match.find('img', class_='ds-mr-2')
            team_1_title = single_match.find('p')
            team_1_run = single_match.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')


            for match_team_2 in single_match.find_all('div', class_='ds-flex ds-items-center ds-min-w-0 ds-mr-1'):
                team_2_flag = match_team_2.find('img', class_='ds-mr-2')
                team_2_title = match_team_2.find('p')

            if single_match.find('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-1'):
                for match_team_3 in single_match.find_all('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-1'):
                    team_2_run = match_team_3.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')

                if team_1_run is not None and team_2_run is not None:
                    if team_1_run.text != team_2_run.text:
                        # print('\nMatch Number:', match_index + 1)
                        # print(match_start.text, match_id.text)
                        # print(team_1_title.text, team_1_run.text)
                        # print(team_2_title.text, team_2_run.text)

                        match = {}
                        match["status"] = match_start.text
                        match["details"] = match_id.text
                        match["team_1_flag"] = team_1_flag['src']
                        match["team_2_flag"] = team_2_flag['src']
                        match["match_link"] = f"{match_link['href']}"
                        match["team_1_title"] = team_1_title.text
                        match["team_1_run"] = team_1_run.text
                        match["team_2_title"] = team_2_title.text
                        match["team_2_run"] = team_2_run.text

                        if match_result is not None:
                            # print(match_result.text)
                            match["result"] = match_result.text

                        # print(match_schedule.text)
                        match["schedule"] = match_schedule.text

                        if match not in out:
                            out.append(match)

                elif team_1_run is not None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text, team_1_run.text)
                    # print(team_2_title.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_1_run"] = team_1_run.text
                    match["team_2_title"] = team_2_title.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                elif team_2_run is not None and team_1_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text, team_2_run.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text
                    match["team_2_run"] = team_2_run.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                elif team_1_run is None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

            if single_match.find('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-1'):
                for match_team_4 in single_match.find_all('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-1'):
                    team_2_run = match_team_4.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')

            #### Printer #######

                if team_1_run is not None and team_2_run is not None:
                    if team_1_run.text != team_2_run.text:
                        # print('\nMatch Number:', match_index + 1)
                        # print(match_start.text, match_id.text)
                        # print(team_1_title.text, team_1_run.text)
                        # print(team_2_title.text, team_2_run.text)

                        match = {}
                        match["status"] = match_start.text
                        match["details"] = match_id.text
                        match["team_1_flag"] = team_1_flag['src']
                        match["team_2_flag"] = team_2_flag['src']
                        match["match_link"] = f"{match_link['href']}"
                        match["team_1_title"] = team_1_title.text
                        match["team_1_run"] = team_1_run.text
                        match["team_2_title"] = team_2_title.text
                        match["team_2_run"] = team_2_run.text

                        if match_result is not None:
                            # print(match_result.text)
                            match["result"] = match_result.text

                        # print(match_schedule.text)
                        match["schedule"] = match_schedule.text

                        if match not in out:
                            out.append(match)

                elif team_1_run is not None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text, team_1_run.text)
                    # print(team_2_title.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_1_run"] = team_1_run.text
                    match["team_2_title"] = team_2_title.text


                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                elif team_2_run is not None and team_1_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text, team_2_run.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text
                    match["team_2_run"] = team_2_run.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                elif team_1_run is None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text)

                    match = {}
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    match["match_link"] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

        print(json.dumps(out))
        with open("match.json", "w") as f:
            f.write(json.dumps(out))

    except socket.error as e:
        print("Error",e)

def match_transfer():
    match_url = "http://localhost:8000/cricket/all_match_api/"
    response = requests.get(match_url)
    matchesdata = response.json()
    url1 = (matchesdata[-1]["match_link"])
    return url1

def connect_to_website(hostname, path):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((hostname, 80))
        print("Connected to", hostname)

        out = []

        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
        client_socket.sendall(request.encode())

        response = client_socket.recv(4096)
        response_text = response.decode()

        location_header = response_text.split('Location: ')[1].split('\r\n')[0]
        print("Location:", location_header)

        req = requests.get(f"{location_header}")
        soup = BeautifulSoup(req.content, 'html.parser')

        for match_details in soup.find_all('div', class_='ds-px-4 ds-py-3 ds-border-b ds-border-line'):
            match_start = match_details.find('strong', class_='ds-uppercase ds-text-tight-m')
            match_id = match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3')
            match_currently = soup.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo')
            match_runrate = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2')

        for about_match in soup.find_all('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3'):
            team_1_name = about_match.find('a', class_='ds-inline-flex ds-items-start ds-leading-none')
            team_1_score = about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap')


        for match_score in soup.find_all(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
            team_2_score = match_score

        batting_table = soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left ds-text-right ds-text-typo-mid3')
        batting_table_head_rows = batting_table.find_all('tr')
        for batting_head_row in batting_table_head_rows:
            batting_head_columns = batting_head_row.find_all('th')
            batting_table_head = [batting_head_column.get_text(strip=True) for batting_head_column in
                                  batting_head_columns]

        bowling_table = soup.find('thead', class_='ds-bg-fill-content-alternate ds-text-left ds-text-right')
        bowling_table_head_rows = bowling_table.find_all('tr')
        for bowling_head_row in bowling_table_head_rows:
            bowling_head_columns = bowling_head_row.find_all('th')
            bowling_table_head = [bowling_head_column.get_text(strip=True) for bowling_head_column in
                                  bowling_head_columns]

        for player in soup.find_all('tbody', class_='ds-text-right'):
            player_all = player.find_all('td')
            player_name = [player_names.get_text(strip=True) for player_names in player_all]

        ball_data = soup.find('div',
                              class_='ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide ds-items-center ds-space-x-2')
        last_ball_list = []
        for data in ball_data.find_all('span'):
            last_ball_list.append(data.text)

        match_details = {}
        match_details['match_start'] = match_start.text
        match_details['match_id'] = match_id.text
        match_details['team_1_name'] = team_1_name.text
        match_details['team_1_score'] = team_1_score.text

        if about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate'):
            team_2_name = about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
            if team_1_name.text != team_2_name.text:
                match_details['team_2_name'] = team_2_name.text

        if about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate !ds-text-typo-mid3'):
            team_2_name = about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate !ds-text-typo-mid3')
            if team_1_name.text != team_2_name.text:
                match_details['team_2_name'] = team_2_name.text

        if team_1_score.text != team_2_score.text:
            match_details['team_2_score'] = team_2_score.text
        match_details['status'] = match_currently.text

        if match_runrate:
            match_details['ran_rate'] = match_runrate.text

        match_details['batting_head'] = batting_table_head

        id = 1
        batting_body_table = soup.find('tbody')
        batting_table_body_rows = batting_body_table.find_all('tr')
        for batting_body_row in batting_table_body_rows:
            batting_body_columns = batting_body_row.find_all('td')
            batting_table_body = [batting_body_column.get_text(strip=True) for batting_body_column in
                                  batting_body_columns]


            match_details[f'batsman_name_{id}'] = batting_table_body
            id += 1

        if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
            match_partnership = soup.find('div',
                                          class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line')

        if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
            match_reviews = soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line')


        match_details['bowling_head'] = bowling_table_head
        match_details['bowler_names'] = player_name

        if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
            match_details['partnership'] = match_partnership.text

        if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
            match_details['reviews'] = match_reviews.text

        match_details['last_30th_balls'] = last_ball_list

        if match_details not in out:
            out.append(match_details)
        print(json.dumps(out))

        with open("match_details.json", "w") as f:
            f.write(json.dumps(out))

    except socket.error as e:
        print("Error:", e)

if __name__ == '__main__':
    while True:
        cricket_api("www.espncricinfo.com")
        url = match_transfer()
        connect_to_website("www.espncricinfo.com",f"{url}")
        time.sleep(2)
