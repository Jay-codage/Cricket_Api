# import socket
# import time
# import requests
# from bs4 import BeautifulSoup
# import json
# import sched
#
#
# def cricket_api(hostname):
#
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     try:
#         client_socket.connect((hostname, 80))
#         print("Connected to", hostname)
#
#         out = []
#
#         request = "GET / HTTP/1.1\r\nHost: " + hostname + "\r\n\r\n"
#         client_socket.sendall(request.encode())
#
#         response = client_socket.recv(4096)
#         response_text = response.decode()
#
#         location_header = response_text.split('Location: ')[1].split('\r\n')[0]
#         print("Location:", location_header)
#
#         req = requests.get(f"{location_header}")
#         soup = BeautifulSoup(req.content, 'html.parser')
#
#         class_tags = {}
#
#         for element in soup.find_all(class_=True):
#             class_names = element.get('class')
#             full_class_name = f"{' '.join(class_names)}"
#             if full_class_name not in class_tags:
#                 class_tags[full_class_name] = []
#             class_tags[full_class_name].append(element.name)
#
#         print(class_tags)
#         keys = list(class_tags.keys())[33]
#         print(keys)
#         values = class_tags[keys][0]
#         print(values)
#
#         id = 1
#         for single_match in soup.find_all(f'{class_tags[list(class_tags.keys())[20]][0]}',class_=f'{list(class_tags.keys())[20]}'):
#             match_start = single_match.find(f'{class_tags[list(class_tags.keys())[26]][0]}',class_=f'{list(class_tags.keys())[26]}')
#             match_id = single_match.find(f'{class_tags[list(class_tags.keys())[27]][0]}',class_=f'{list(class_tags.keys())[27]}')
#             match_result = single_match.find(f'{class_tags[list(class_tags.keys())[36]][0]}',class_=f'{list(class_tags.keys())[36]}')
#             match_schedule = single_match.find(f'{class_tags[list(class_tags.keys())[37]][0]}',class_=f'{list(class_tags.keys())[37]}')
#             match_link = single_match.find(f'{class_tags[list(class_tags.keys())[21]][0]}',class_=f'{list(class_tags.keys())[21]}')
#             match_links = match_link['href']
#             match_link_slug = match_links.replace('/', '-')
#
#             team_1_flag = single_match.find(f'{class_tags[list(class_tags.keys())[34]][0]}',class_=f'{list(class_tags.keys())[34]}')
#             team_1_title = single_match.find(f'{class_tags[list(class_tags.keys())[35]][0]}')
#             team_1_run = single_match.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
#
#             for match_team_2 in single_match.find_all(f'{class_tags[list(class_tags.keys())[33]][0]}', class_=f'{list(class_tags.keys())[33]}'):
#                 team_2_flag = match_team_2.find(f'{class_tags[list(class_tags.keys())[34]][0]}', class_=f'{list(class_tags.keys())[34]}')
#                 team_2_title = match_team_2.find(f'{class_tags[list(class_tags.keys())[35]][0]}')
#
#             if single_match.find('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-1'):
#                 for match_team_3 in single_match.find_all('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-1'):
#                     team_2_run = match_team_3.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
#
#                 if team_1_run is not None and team_2_run is not None:
#                     if team_1_run.text != team_2_run.text:
#                         # print('\nMatch Number:', match_index + 1)
#                         # print(match_start.text, match_id.text)
#                         # print(team_1_title.text, team_1_run.text)
#                         # print(team_2_title.text, team_2_run.text)
#
#                         match = {}
#                         match['match_id'] = id
#                         match["status"] = match_start.text
#                         match["details"] = match_id.text
#                         match["team_1_flag"] = team_1_flag['src']
#                         match["team_2_flag"] = team_2_flag['src']
#                         match["match_link"] = f"{match_link['href']}"
#                         match['match_link_slug'] = f"{match_link_slug}"
#                         match['match_scorecard_link'] = f"{match_link['href']}"
#                         match["team_1_title"] = team_1_title.text
#                         match["team_1_run"] = team_1_run.text
#                         match["team_2_title"] = team_2_title.text
#                         match["team_2_run"] = team_2_run.text
#
#                         if match_result is not None:
#                             # print(match_result.text)
#                             match["result"] = match_result.text
#
#                         # print(match_schedule.text)
#                         match["schedule"] = match_schedule.text
#
#                         if match not in out:
#                             out.append(match)
#
#                         id += 1
#
#                 elif team_1_run is not None and team_2_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text, team_1_run.text)
#                     # print(team_2_title.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_1_run"] = team_1_run.text
#                     match["team_2_title"] = team_2_title.text
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#                 elif team_2_run is not None and team_1_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text)
#                     # print(team_2_title.text, team_2_run.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_2_title"] = team_2_title.text
#                     match["team_2_run"] = team_2_run.text
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#                 elif team_1_run is None and team_2_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text)
#                     # print(team_2_title.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_2_title"] = team_2_title.text
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#             if single_match.find('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-1'):
#                 for match_team_4 in single_match.find_all('div',class_='ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-1'):
#                     team_2_run = match_team_4.find('div',class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
#
#             #### Printer #######
#
#                 if team_1_run is not None and team_2_run is not None:
#                     if team_1_run.text != team_2_run.text:
#                         # print('\nMatch Number:', match_index + 1)
#                         # print(match_start.text, match_id.text)
#                         # print(team_1_title.text, team_1_run.text)
#                         # print(team_2_title.text, team_2_run.text)
#
#                         match = {}
#                         match['match_id'] = id
#                         match["status"] = match_start.text
#                         match["details"] = match_id.text
#                         match["team_1_flag"] = team_1_flag['src']
#                         match["team_2_flag"] = team_2_flag['src']
#                         match["match_link"] = f"{match_link['href']}"
#                         match['match_link_slug'] = f"{match_link_slug}"
#                         match['match_scorecard_link'] = f"{match_link['href']}"
#                         match["team_1_title"] = team_1_title.text
#                         match["team_1_run"] = team_1_run.text
#                         match["team_2_title"] = team_2_title.text
#                         match["team_2_run"] = team_2_run.text
#
#                         if match_result is not None:
#                             # print(match_result.text)
#                             match["result"] = match_result.text
#
#                         # print(match_schedule.text)
#                         match["schedule"] = match_schedule.text
#
#                         if match not in out:
#                             out.append(match)
#
#                         id += 1
#
#                 elif team_1_run is not None and team_2_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text, team_1_run.text)
#                     # print(team_2_title.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_1_run"] = team_1_run.text
#                     match["team_2_title"] = team_2_title.text
#
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#                 elif team_2_run is not None and team_1_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text)
#                     # print(team_2_title.text, team_2_run.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_2_title"] = team_2_title.text
#                     match["team_2_run"] = team_2_run.text
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#                 elif team_1_run is None and team_2_run is None:
#                     # print('\nMatch Number:', match_index + 1)
#                     # print(match_start.text, match_id.text)
#                     # print(team_1_title.text)
#                     # print(team_2_title.text)
#
#                     match = {}
#                     match['match_id'] = id
#                     match["status"] = match_start.text
#                     match["details"] = match_id.text
#                     match["team_1_flag"] = team_1_flag['src']
#                     match["team_2_flag"] = team_2_flag['src']
#                     match["match_link"] = f"{match_link['href']}"
#                     match['match_link_slug'] = f"{match_link_slug}"
#                     match['match_scorecard_link'] = f"{match_link['href']}"
#                     match["team_1_title"] = team_1_title.text
#                     match["team_2_title"] = team_2_title.text
#
#                     if match_result is not None:
#                         # print(match_result.text)
#                         match["result"] = match_result.text
#
#                     # print(match_schedule.text)
#                     match["schedule"] = match_schedule.text
#
#                     if match not in out:
#                         out.append(match)
#
#                     id += 1
#
#         print(json.dumps(out))
#         with open("match.json", "w") as f:
#             f.write(json.dumps(out))
#
#         id +=1
#
#     except socket.error as e:
#         print("Error",e)
#
# if __name__ == '__main__':
#     while True:
#         cricket_api("www.espncricinfo.com")
#         time.sleep(2)



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

        id = 1
        for single_match in soup.find_all('div',class_='ds-p-2 ds-bg-fill-hsb-scorecell ds-text-compact-2xs ds-rounded-xl ds-h-[146px]'):
            match_start = single_match.find('span', class_='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5')
            match_id = single_match.find('span', class_='ds-text-tight-xs ds-text-typo-mid2')
            match_result = single_match.find('p', class_='ds-text-tight-xs ds-truncate ds-text-typo')
            match_schedule = single_match.find('div',class_='ds-flex ds-mt-2 ds-pt-1.5 ds-border-t ds-border-line-default-translucent')
            match_link = single_match.find('a',class_='ds-no-tap-higlight')
            match_links = match_link['href']
            match_link_slug = match_links.replace('/','-')

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
                        match['match_id'] = id
                        match["status"] = match_start.text
                        match["details"] = match_id.text
                        match["team_1_flag"] = team_1_flag['src']
                        match["team_2_flag"] = team_2_flag['src']
                        if (match_link['href']) is not None:
                            match["match_link"] = f"{match_link['href']}"
                        match['match_link_slug'] = f"{match_link_slug}"
                        match['match_scorecard_link'] = f"{match_link['href']}"
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

                        id += 1

                elif team_1_run is not None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text, team_1_run.text)
                    # print(team_2_title.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
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

                    id += 1

                elif team_2_run is not None and team_1_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text, team_2_run.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
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

                    id += 1

                elif team_1_run is None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                    id += 1

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
                        match['match_id'] = id
                        match["status"] = match_start.text
                        match["details"] = match_id.text
                        match["team_1_flag"] = team_1_flag['src']
                        match["team_2_flag"] = team_2_flag['src']
                        if (match_link['href']) is not None:
                            match["match_link"] = f"{match_link['href']}"
                        match['match_link_slug'] = f"{match_link_slug}"
                        match['match_scorecard_link'] = f"{match_link['href']}"
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

                        id += 1

                elif team_1_run is not None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text, team_1_run.text)
                    # print(team_2_title.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
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

                    id += 1

                elif team_2_run is not None and team_1_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text, team_2_run.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
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

                    id += 1

                elif team_1_run is None and team_2_run is None:
                    # print('\nMatch Number:', match_index + 1)
                    # print(match_start.text, match_id.text)
                    # print(team_1_title.text)
                    # print(team_2_title.text)

                    match = {}
                    match['match_id'] = id
                    match["status"] = match_start.text
                    match["details"] = match_id.text
                    match["team_1_flag"] = team_1_flag['src']
                    match["team_2_flag"] = team_2_flag['src']
                    if (match_link['href']) is not None:
                        match["match_link"] = f"{match_link['href']}"
                    match['match_link_slug'] = f"{match_link_slug}"
                    match['match_scorecard_link'] = f"{match_link['href']}"
                    match["team_1_title"] = team_1_title.text
                    match["team_2_title"] = team_2_title.text

                    if match_result is not None:
                        # print(match_result.text)
                        match["result"] = match_result.text

                    # print(match_schedule.text)
                    match["schedule"] = match_schedule.text

                    if match not in out:
                        out.append(match)

                    id += 1

        print(json.dumps(out))
        with open("match.json", "w") as f:
            f.write(json.dumps(out))

        id +=1

    except socket.error as e:
        print("Error",e)

if __name__ == '__main__':
    while True:
        cricket_api("www.espncricinfo.com")
        time.sleep(5)



