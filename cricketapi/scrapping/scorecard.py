import requests
import socket
import time
from bs4 import BeautifulSoup
import json
import concurrent.futures

def collect_scorecard_link():
    all_links = set()

    with open('match_details.json', 'r') as file:
        data = json.load(file)
        match_links = [item['match_scorecard_link'] for item in data if
                       item['match_scorecard_link'].endswith('/full-scorecard')]
        all_links.update(match_links)

    with open('match.json', 'r') as file:
        data = json.load(file)
        match_links = [item['match_scorecard_link'] for item in data if
                       item['match_scorecard_link'].endswith('/full-scorecard')]
        all_links.update(match_links)

    return (list(all_links))

def match_scorecard(url):

    try:
        req = requests.get(f"{url}")
        soup = BeautifulSoup(req.content, 'html.parser')

        scorecard = {} # match scorecard dic

############## Match details ##############

        for match_details in soup.find_all('div', class_='ds-px-4 ds-py-3 ds-border-b ds-border-line'):

            if match_details.find('strong', class_='ds-uppercase ds-text-tight-m'):
                match_start = match_details.find('strong', class_='ds-uppercase ds-text-tight-m')
                scorecard['match_start'] = match_start.text

            if match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3'):
                match_id = match_details.find('div', class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3')
                scorecard['match_id'] = match_id.text

            if match_details.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo'):
                match_currently = soup.find('p', class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo')
                scorecard['status'] = match_currently.text

            if match_details.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2'):
                match_runrate = soup.find('div',class_='ds-text-tight-s ds-font-regular ds-overflow-x-auto ds-scrollbar-hide ds-whitespace-nowrap ds-mt-1 md:ds-mt-0 lg:ds-flex lg:ds-items-center lg:ds-justify-between lg:ds-px-4 lg:ds-py-2 lg:ds-bg-fill-content-alternate ds-text-typo-mid3 md:ds-text-typo-mid2')
                scorecard['ran_rate'] = match_runrate.text
        for matches_links in soup.find('div',class_="ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line"):
            if matches_links.find('div',class_='ds-shrink-0'):
                match_links = matches_links.find('a')
                match_linkes = match_links['href']
                match_link = match_linkes.replace('/', '-')
                scorecard['match_link'] = f"{match_linkes}"
                scorecard['match_link_slug'] = f"{match_link}"
                match_s_linkes = match_linkes.replace('live-cricket-score', 'full-scorecard')
                scorecard['match_scorecard_link'] = f"{match_s_linkes}"
                match_s_link_slug = match_link.replace('live-cricket-score', 'full-scorecard')
                scorecard['match_scorecard_link_slug'] = f"{match_s_link_slug}"

        team_name_dic = {}
        for about_match in soup.find_all('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3'):
            if about_match.find_all('a', class_='ds-inline-flex ds-items-start ds-leading-none'):
                team_names = about_match.find_all('a', class_='ds-inline-flex ds-items-start ds-leading-none')
                team_1_name = team_names[0].text.strip()
                team_2_name = team_names[1].text.strip()

                team_name_dic['team_1_name'] = team_1_name
                team_name_dic['team_2_name'] = team_2_name

                break

        scorecard['team_1_name'] = team_name_dic['team_1_name']
        scorecard['team_2_name'] = team_name_dic['team_2_name']

        for about_match in soup.find_all('div', class_='ds-text-compact-xxs ds-p-2 ds-px-4 lg:ds-py-3'):

            if about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
                team_1_score = about_match.find('div',class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap')
                scorecard['team_1_score'] = team_1_score.text

            if about_match.find('p',class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo'):
                match_result = about_match.find('p',class_='ds-text-tight-m ds-font-regular ds-truncate ds-text-typo')
                scorecard['result'] = match_result.text

        if soup.find(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
            for match_score in soup.find_all(class_='ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap'):
                team_2_score = match_score

            if team_1_score.text != team_2_score.text:
                scorecard['team_2_score'] = team_2_score.text

        id = 1
        for match_table in soup.find_all("div", class_="ds-rounded-lg ds-mt-2"):
            table_head = match_table.find('span', class_='ds-text-title-xs ds-font-bold ds-text-typo')
            inning_titles = table_head.text
            inning_title = f'match_innings_{id}'
            scorecard[inning_title] = {
                'table_head': [inning_titles],
                'batting_head': [],
                'batting': [],
                'extra': [],
                'bowling_head': [],
                'bowling': []
            }

            id += 1
            table_1 = match_table.find('thead')
            for batting_table_tr in table_1.find_all('tr'):
                batting_table_th = batting_table_tr.find_all('th')
                batting_table_head = [batting_table.get_text(strip=True) for batting_table in batting_table_th]
                scorecard[inning_title]['batting_head'] = batting_table_head

            batting_table_tbody = match_table.find('tbody')
            for batting_table_tbody_tr in batting_table_tbody.find_all('tr', class_=''):
                batting_table_tbody_td = batting_table_tbody_tr.find_all('td')
                batting_table_body = [batting_body.get_text(strip=True) for batting_body in batting_table_tbody_td]
                scorecard[inning_title]['batting'].append(batting_table_body)

            for batting_table_tbody_tr in batting_table_tbody.find_all('tr', class_='ds-text-tight-s'):
                batting_table_tbody_td = batting_table_tbody_tr.find_all('td')
                batting_table_body = [batting_body.get_text(strip=True) for batting_body in batting_table_tbody_td]
                scorecard[inning_title]['extra'].append(batting_table_body)

            for table_1 in match_table.find_all('thead'):
                for batting_table_tr in table_1.find_all('tr'):
                    batting_table_th = batting_table_tr.find_all('th')
                    batting_table_head = [batting_table.get_text(strip=True) for batting_table in batting_table_th]
                    scorecard[inning_title]['bowling_head'] = batting_table_head

            bowling_body = match_table.find("table", class_="ds-w-full ds-table ds-table-md ds-table-auto")
            bowling_body_head = bowling_body.find("tbody")
            rows = bowling_body_head.find_all("tr", class_='')
            bowling_data = []
            for row in rows:
                cols = row.find_all("td")
                bowling = [col.get_text(strip=True) for col in cols]
                bowling_data.append(bowling)

            scorecard[inning_title]['bowling'] = bowling_data

        return scorecard

    except socket.error as e:
        print("Error name: ",e)

def main():
    hostname = "www.espncricinfo.com"
    urls = collect_scorecard_link()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(match_scorecard,f"http://{hostname}{url}"): url for url in urls}

        out = []
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if data:
                out.append(data)
            print(out)

        with open("scorecard.json",'w') as f:
            f.write(json.dumps(out))

if __name__ == '__main__':
    while True:
        main()
    time.sleep(2)






# for matches_links in soup.find('div',class_="ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line"):
        #     for matches_linkes in matches_links.find_all('div',class_='ds-shrink-0'):
        #         match_links = matches_linkes.find('a',class_='ds-flex ds-justify-center active:ds-bg-ui-fill-hover focus:ds-bg-ui-fill-hover ds-h-10')
        #         if match_links:
        #             linkes_href = match_links['href']
        #             if linkes_href.endswith('/live-cricket-score'):
        #                 match_live_link = linkes_href
        #                 match_live_link_slug = match_live_link.replace('/','-')
        #                 scorecard['match_link'] = f"{match_live_link}"
        #                 scorecard['match_link_slug'] = f"{match_live_link_slug}"
        #             if linkes_href.endswith('/full-scorecard'):
        #                 match_live_link = linkes_href
        #                 match_live_link_slug = match_live_link.replace('/', '-')
        #                 scorecard['match_scorecard_link']= f"{match_live_link}"
        #                 scorecard['match_scorecard_link_slug'] = f"{match_live_link_slug}"






# ############ team 1 scorecard table ###################
#
#         ######### team 1 batting ########
#
#         team_1 = {}  # team 1 dic
#         table_head = []  # Both team table head
#         for head in soup.find_all('div', class_='ds-rounded-lg ds-mt-2'):
#             head_1 = head.find('span',class_='ds-text-title-xs ds-font-bold ds-text-typo')
#             table_main_head = head_1.text.replace('\u00a0',' ')
#             table_head.append(table_main_head)
#         scorecard['team_table_head'] = table_head
#
#         batting_table = soup.find('thead',class_='ds-bg-fill-content-alternate ds-text-left')
#         batting_table_head_rows = batting_table.find_all('tr',class_='ds-text-right')
#         for batting_head_row in batting_table_head_rows:
#             batting_head_columns = batting_head_row.find_all('th')
#             batting_table_head = [batting_head_column.get_text(strip=True).replace('\u2020', '') for batting_head_column in batting_head_columns]
#
#             scorecard['batting_head'] = batting_table_head
#
#         batting_body_table = soup.find('tbody')
#         batting_table_body_rows = batting_body_table.find_all('tr',class_='')
#         batting_table_body_rows_extras = batting_body_table.find_all('tr',class_='ds-text-tight-s')
#         batsman_names = [] # team 1 batsman name
#         for batting_body_row in batting_table_body_rows:
#             batting_body_columns = batting_body_row.find_all('td')
#             batting_table_body = [batting_body_column.get_text(strip=True).replace('\u2020', '') for batting_body_column in batting_body_columns]
#             batsman_names.append(batting_table_body)
#
#         for extra in batting_table_body_rows_extras:
#             batting_table_body_rows_extra = extra.find_all('td')
#             batting_table_body_extra = [batting_body_column_extra.get_text(strip=True).replace('\u2020', '') for batting_body_column_extra in batting_table_body_rows_extra]
#             batsman_names.append(batting_table_body_extra)
#
#         batting_table_body_rows_extras = batting_body_table.find_all('tr',class_='!ds-border-b-0')
#         for extra in batting_table_body_rows_extras:
#             batting_table_body_rows_extra = extra.find_all('td')
#             batting_table_body_extra = [batting_body_column_extra.get_text(strip=True).replace('\u2020', '') for batting_body_column_extra in batting_table_body_rows_extra]
#             batsman_names.append(batting_table_body_extra)
#
#         team_1['batting'] = batsman_names
#         # print(batsman_names)
#
#         ########## team 1 bowling #########
#
#         bowling_body = soup.find("table", class_="ds-w-full ds-table ds-table-md ds-table-auto")
#         bowling_table_head = bowling_body.find("thead")
#         table_row = bowling_table_head.find_all("tr")
#         for table_rows in table_row:
#             ball_head = table_rows.find_all("th")
#             ball_table_head = [bowling_head.get_text(strip=True).replace('\u2020', '') for bowling_head in ball_head]
#
#             scorecard['bowling_head'] = ball_table_head
#
#         bowling_body_head = bowling_body.find("tbody")
#         rows = bowling_body_head.find_all("tr",class_='')
#         bowling = []  # team 1 bowler name
#         for row in rows:
#             cols = row.find_all("td")
#             bowling.append([col.get_text(strip=True).replace('\u2020', '') for col in cols])
#
#         team_1['bowling'] = bowling
#         scorecard['team_1'] = team_1
#         # print(bowling)
#
# ############ team 2 scorecard ####################
#
#         out_1 = [] # Both team table list
#         out_2 = [] # team 2 table list
#         for table in soup.find_all('div',class_='ds-rounded-lg ds-mt-2'):
#             for tbody in table.find_all("tbody"):
#                 rows = tbody.find_all("tr",class_='')
#                 for row in rows:
#                     cols = row.find_all("td")
#                     batsman = [batsmans.get_text(strip=True).replace('\u2020', '') for batsmans in cols ]
#                     if batsman not in out_1:
#                         out_1.append(batsman)
#
#                 rows = tbody.find_all("tr",class_='ds-text-tight-s')
#                 for row in rows:
#                     cols = row.find_all("td")
#                     batsman = [batsmans.get_text(strip=True).replace('\u2020', '') for batsmans in cols]
#                     if batsman not in out_1:
#                         out_1.append(batsman)
#
#                 rows = tbody.find_all("tr",class_='!ds-border-b-0')
#                 for row in rows:
#                     cols = row.find_all("td")
#                     batsman = [batsmans.get_text(strip=True).replace('\u2020', '') for batsmans in cols]
#                     if batsman not in out_1:
#                         out_1.append(batsman)
#
#         # print(json.dumps(out_1))
#
#         for item in out_1:
#             if item not in batsman_names and item not in bowling:
#                 out_2.append(item)
#
#         # print(out_2)
#
#         ########## team 2 batting ########
#
#         batting = []  # team 2 batsman list
#         team_2 = {}  # team 2 table dic
#         for sublist in out_2:
#             if sublist[0] == "TOTAL":
#                 break
#             batting.append(sublist)
#         # print(batting)
#
#         ########### team 2 bowling ##########
#
#         bowlings = [] # team 2 bowler list(revers)
#         for sublist in reversed(out_2):
#             if len(sublist) == 11:
#                 bowlings.append(sublist)
#
#         bowling = [] # team 2 bowler list (main)
#         for data in reversed(bowlings):
#             bowling.append(data)
#         # print(bowling)
#
#         for item in out_2:
#             if item not in batting and item not in bowling:
#                 batting.append(item)
#         team_2['batting'] = batting
#         team_2['bowling'] = bowling
#         scorecard['team_2'] = team_2
#         # print(batting)




