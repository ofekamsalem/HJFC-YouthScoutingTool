
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urljoin
from selenium import webdriver

import json

""""
it works! we have list of players with names and their IDS
"""

# load  config.json file
def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_players_names_and_ID(team_id):
    config = load_config()
    base_players_list_url = config['base team_players list url']
    players_list_url = base_players_list_url.format(team_id=team_id)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,20)
    driver.get(players_list_url)
    container = driver.find_elements(By.CSS_SELECTOR, "#teamPlayers ul li")
    players_IDS = []
    players_names = []
    players_names_and_IDS = {}
    for li in container:
        a = li.find_element(By.CSS_SELECTOR, 'a[href*="player_id="]')
        href = a.get_attribute("href")
        href = urljoin(players_list_url, href)   # normalize relative link
        qs = parse_qs(urlparse(href).query)
        player_id = qs.get("player_id", [""])[0]
        players_IDS.append(player_id)
        name = li.find_element(By.CSS_SELECTOR, "div.text").text.strip()
        players_names.append(name)
        players_names_and_IDS[player_id] = name
    driver.quit()
    return players_names_and_IDS

