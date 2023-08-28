import requests
import socket
import time
from bs4 import BeautifulSoup
import json
import concurrent.futures

def collect_scorecard_link():
    all_links = set()
    try:
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
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle the case when the file is not found or contains invalid JSON data
        print(f"Error reading or processing ")
        pass

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
        future_to_url = {executor.submit(match_scorecard, f"http://{hostname}{url}"): url for url in urls}

        out = []
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                if data:
                    out.append(data)
                print(out)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")

        # Serialize the data to JSON and write it to a file
        with open("scorecard.json", 'w') as f:
            json.dump(out, f, indent=4)


if __name__ == '__main__':
    while True:
        main()
    time.sleep(5)

