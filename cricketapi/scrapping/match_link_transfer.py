import socket
import time
import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures

def collect_match_link():
    for file_name in ['match.json']:
        try:
            with open('match.json', 'r') as file:
                data = json.load(file)
                match_links = [item['match_link'] for item in data if item['match_link'].endswith('/live-cricket-score')]
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case when the file is not found or contains invalid JSON data
            print(f"Error reading or processing {file_name}")
            pass
    return (match_links)


def connect_to_website(url):

    try:
        req = requests.get(f"{url}")
        if req.status_code == 200 and req.content:
            soup = BeautifulSoup(req.content, 'html.parser')


            id = 1

            match_detail = {}

            for match_details in soup.find_all('div', class_='ds-px-4 ds-py-3 ds-border-b ds-border-line'):

                if match_details.find('strong', class_='ds-uppercase ds-text-tight-m'):
                    match_start = match_details.find('strong', class_='ds-uppercase ds-text-tight-m')
                    match_detail['match_id']=id
                    match_detail['match_start'] = match_start.text

                if match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3'):
                    match_about = match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3')
                    match_detail['match_about'] = match_about.text

                if match_details.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo'):
                    match_currently = soup.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo')
                    match_detail['status'] = match_currently.text

                if match_details.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2'):
                    match_runrate = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2')
                    match_detail['ran_rate'] = match_runrate.text

            for match in soup.find('div',class_='ds-relative ds-w-full ds-scrollbar-hide ds-border-t ds-border-line ds-px-2 ds-flex ds-bg-fill-content-prime ds-overflow-x-auto ds-scrollbar-hide'):
                if match.find('div',class_='ds-shrink-0'):
                    matches = match.find('div',class_='ds-shrink-0')
                    if matches.find('a'):
                        match_links = matches.find('a')
                        match_linkes = match_links['href']
                        match_link = match_linkes.replace('/', '-')
                        match_detail['match_link'] = f"{match_linkes}"
                        match_detail['match_link_slug'] = f"{match_link}"
                        match_s_linkes = match_linkes.replace('live-cricket-score', 'full-scorecard')
                        match_detail['match_scorecard_link'] = f"{match_s_linkes}"
                        match_s_link_slug = match_link.replace('live-cricket-score', 'full-scorecard')
                        match_detail['match_scorecard_link_slug'] = f"{match_s_link_slug}"

            # for matches_links in soup.find('div',class_="ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide"):
            #     if matches_links.find('div',class_='ds-shrink-0'):
            #         match_links = matches_links.find('a')
            #         match_linkes = match_links['href']
            #         match_link = match_linkes.replace('/', '-')
            #         print(match_linkes)
            #         match_detail['match_link'] = f"{match_linkes}"
            #         match_detail['match_link_slug'] = f"{match_link}"
            #         match_s_linkes = match_linkes.replace('live-cricket-score', 'full-scorecard')
            #         match_detail['match_scorecard_link'] = f"{match_s_linkes}"
            #         match_s_link_slug = match_link.replace('live-cricket-score', 'full-scorecard')
            #         match_detail['match_scorecard_link_slug'] = f"{match_s_link_slug}"

            team_name_dic = {}
            for about_match in soup.find_all('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3'):
                if about_match.find_all('a', class_='ds-inline-flex ds-items-start ds-leading-none'):
                    team_names = about_match.find_all('a', class_='ds-inline-flex ds-items-start ds-leading-none')
                    team_1_name = team_names[0].text.strip()
                    team_2_name = team_names[1].text.strip()

                    team_name_dic['team_1_name'] = team_1_name
                    team_name_dic['team_2_name'] = team_2_name

                    break

            match_detail['team_1_name'] = team_name_dic['team_1_name']
            match_detail['team_2_name'] = team_name_dic['team_2_name']

            if about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
                team_1_score = about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap')
                match_detail['team_1_score'] = team_1_score.text

            if soup.find(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
                for match_score in soup.find_all(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
                    team_2_score = match_score

                if team_1_score.text != team_2_score.text:
                    match_detail['team_2_score'] = team_2_score.text

            if soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left ds-text-right ds-text-typo-mid3'):
                batting_table = soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left ds-text-right ds-text-typo-mid3')
                batting_table_head_rows = batting_table.find_all('tr')
                for batting_head_row in batting_table_head_rows:
                    batting_head_columns = batting_head_row.find_all('th')
                    batting_table_head = [batting_head_column.get_text(strip=True) for batting_head_column in batting_head_columns]

                    match_detail['batting_head'] = batting_table_head

            if soup.find('tbody'):
                id = 1
                batting_body_table = soup.find('tbody')
                batting_table_body_rows = batting_body_table.find_all('tr')
                for batting_body_row in batting_table_body_rows:
                    batting_body_columns = batting_body_row.find_all('td')
                    batting_table_body = [batting_body_column.get_text(strip=True) for batting_body_column in batting_body_columns]

                    match_detail[f'batsman_name_{id}'] = batting_table_body
                    id += 1

            if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
                match_partnership = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line')

            if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
                match_reviews = soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line')

            if soup.find('thead', class_='ds-bg-fill-content-alternate ds-text-left ds-text-right'):
                bowling_table = soup.find('thead', class_='ds-bg-fill-content-alternate ds-text-left ds-text-right')
                bowling_table_head_rows = bowling_table.find_all('tr')
                for bowling_head_row in bowling_table_head_rows:
                    bowling_head_columns = bowling_head_row.find_all('th')
                    bowling_table_head = [bowling_head_column.get_text(strip=True) for bowling_head_column in bowling_head_columns]

                    match_detail['bowling_head'] = bowling_table_head

            for player in soup.find_all('tbody', class_='ds-text-right'):
                player_all = player.find_all('td')
                player_name = [player_names.get_text(strip=True) for player_names in player_all]

                match_detail['bowler_names'] = player_name

            if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
                match_detail['partnership'] = match_partnership.text

            if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
                match_detail['reviews'] = match_reviews.text

            if soup.find('div',class_='ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide ds-items-center ds-space-x-2'):
                ball_data = soup.find('div',class_='ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide ds-items-center ds-space-x-2')
                last_ball_list = []
                for data in ball_data.find_all('span'):
                    last_ball_list.append(data.text)

                match_detail['last_30th_balls'] = last_ball_list

            id += 1

            return match_detail

        else:
            print("Invalid response:", req.status_code)

    except socket.error as e:
        print("Error:", e)
        return None


def main():
    hostname = "www.espncricinfo.com"
    urls = collect_match_link()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(connect_to_website,f"http://{hostname}{url}"): url for url in urls}

        out = []
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if data:
                out.append(data)
            print(out)

        with open("match_details.json",'w') as f:
            f.write(json.dumps(out))

if __name__ == '__main__':
    while True:
        main()
    time.sleep(1)



# class_tags = {}
#
# for element in soup.find_all(class_=True):
#     class_names = element.get('class')
#     full_class_name = f"{' '.join(class_names)}"
#     if full_class_name not in class_tags:
#         class_tags[full_class_name] = []
#     class_tags[full_class_name].append(element.name)

# print(class_tags)
# keys = list(class_tags.keys())[69]
# print(keys)
# values = class_tags[keys][0]
# print(values)
# print("hello")
# print("hello")

# Find the index of a specific key
# key_to_find = 'ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'
#
# try:
#     index = list(class_tags.keys()).index(key_to_find)
#     print(f"The index of '{key_to_find}' in the dictionary is: {index}")
# except ValueError:
#     print(f"'{key_to_find}' was not found in the dictionary.")


# import socket
# import time
# import requests
# from bs4 import BeautifulSoup
# import json
#
#
# def connect_to_website(hostname, urls):
#     for url in urls:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         try:
#             client_socket.connect((hostname, 80))
#             print("Connected to", hostname)
#
#             out = []
#
#             request = f"GET {url} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
#             client_socket.sendall(request.encode())
#
#             response = client_socket.recv(4096)
#             response_text = response.decode()
#             # print(response_text)
#
#             location_header = response_text.split('Location: ')[1].split('\r\n')[0]
#             print("Location:", location_header)
#
#             req = requests.get(f"{location_header}")
#             soup = BeautifulSoup(req.content, 'html.parser')
#
#             match_detail = {}
#
#             for match_details in soup.find_all('div', class_='ds-px-4 ds-py-3 ds-border-b ds-border-line'):
#
#                 if match_details.find('strong', class_='ds-uppercase ds-text-tight-m'):
#                     match_start = match_details.find('strong', class_='ds-uppercase ds-text-tight-m')
#                     match_detail['match_start'] = match_start.text
#
#                 if match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3'):
#                     match_about = match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3')
#                     match_detail['match_about'] = match_about.text
#
#                 if match_details.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo'):
#                     match_currently = soup.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo')
#                     match_detail['status'] = match_currently.text
#
#                 if match_details.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2'):
#                     match_runrate = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2')
#                     match_detail['ran_rate'] = match_runrate.text
#
#             for about_match in soup.find_all('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3'):
#
#                 if about_match.find('a', class_='ds-inline-flex ds-items-start ds-leading-none'):
#                     team_1_name = about_match.find('a', class_='ds-inline-flex ds-items-start ds-leading-none')
#                     match_detail['team_1_name'] = team_1_name.text
#
#                 if about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
#                     team_1_score = about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap')
#                     match_detail['team_1_score'] = team_1_score.text
#
#             if soup.find(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
#                 for match_score in soup.find_all(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
#                     team_2_score = match_score
#
#                 if team_1_score.text != team_2_score.text:
#                     match_detail['team_2_score'] = team_2_score.text
#
#             if about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate'):
#                 team_2_name = about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
#                 if team_1_name.text != team_2_name.text:
#                     match_detail['team_2_name'] = team_2_name.text
#
#             if about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate !ds-text-typo-mid3'):
#                 team_2_name = about_match.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate !ds-text-typo-mid3')
#                 if team_1_name.text != team_2_name.text:
#                     match_detail['team_2_name'] = team_2_name.text
#
#
#             if soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left ds-text-right ds-text-typo-mid3'):
#                 batting_table = soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left ds-text-right ds-text-typo-mid3')
#                 batting_table_head_rows = batting_table.find_all('tr')
#                 for batting_head_row in batting_table_head_rows:
#                     batting_head_columns = batting_head_row.find_all('th')
#                     batting_table_head = [batting_head_column.get_text(strip=True) for batting_head_column in batting_head_columns]
#
#                     match_detail['batting_head'] = batting_table_head
#
#             if soup.find('tbody'):
#                 id = 1
#                 batting_body_table = soup.find('tbody')
#                 batting_table_body_rows = batting_body_table.find_all('tr')
#                 for batting_body_row in batting_table_body_rows:
#                     batting_body_columns = batting_body_row.find_all('td')
#                     batting_table_body = [batting_body_column.get_text(strip=True) for batting_body_column in batting_body_columns]
#
#                     match_detail[f'batsman_name_{id}'] = batting_table_body
#                     id += 1
#
#             if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
#                 match_partnership = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line')
#
#             if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
#                 match_reviews = soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line')
#
#             if soup.find('thead', class_='ds-bg-fill-content-alternate ds-text-left ds-text-right'):
#                 bowling_table = soup.find('thead', class_='ds-bg-fill-content-alternate ds-text-left ds-text-right')
#                 bowling_table_head_rows = bowling_table.find_all('tr')
#                 for bowling_head_row in bowling_table_head_rows:
#                     bowling_head_columns = bowling_head_row.find_all('th')
#                     bowling_table_head = [bowling_head_column.get_text(strip=True) for bowling_head_column in bowling_head_columns]
#
#                     match_detail['bowling_head'] = bowling_table_head
#
#             for player in soup.find_all('tbody', class_='ds-text-right'):
#                 player_all = player.find_all('td')
#                 player_name = [player_names.get_text(strip=True) for player_names in player_all]
#
#                 match_detail['bowler_names'] = player_name
#
#             if soup.find('div', class_='ds-text-tight-s ds-font-regular ds-px-4 ds-py-2 ds-border-y ds-border-line'):
#                 match_detail['partnership'] = match_partnership.text
#
#             if soup.find('div', class_='ds-flex ds-items-center ds-border-b ds-border-line'):
#                 match_detail['reviews'] = match_reviews.text
#
#             if soup.find('div',class_='ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide ds-items-center ds-space-x-2'):
#                 ball_data = soup.find('div',class_='ds-flex ds-flex-row ds-w-full ds-overflow-x-auto ds-scrollbar-hide ds-items-center ds-space-x-2')
#                 last_ball_list = []
#                 for data in ball_data.find_all('span'):
#                     last_ball_list.append(data.text)
#
#                 match_detail['last_30th_balls'] = last_ball_list
#
#             if match_detail not in out:
#                 out.append(match_detail)
#             print(json.dumps(out))
#
#             with open("match_details.json", "w") as f:
#                 f.write(json.dumps(out))
#
#         except socket.error as e:
#             print("Error:", e)
#
#
# while True:
#     hostname = "www.espncricinfo.com"
#     urls = ["/series/the-ashes-2023-1336037/england-vs-australia-5th-test-1336047/live-cricket-score",
#             ]
#     connect_to_website(hostname,urls)
#     time.sleep(0.1)
