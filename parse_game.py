from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urljoin
from selenium import webdriver
import json
import re
from create_team import team_creation
from team import Team
MATCH_DURATION = 90


# load config.json file
def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    

def parse_games() -> Team:
    team = team_creation()

    # iterate over all the team's games:
    for game in team.games:
        parse_game(game.game_ID, game.date, team)
    for pid in team.team_players.keys():
        print(team.team_players[pid].involvements)
        print("number of involvements:", len(team.team_players[pid].involvements))
        print(team.team_players[pid].player_name)
    return team




def parse_game(game_id, date, team: Team):
    config = load_config()
    base_game_url = config['base game url']
    game_url = base_game_url.format(game_id=game_id)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,20)
    driver.get(game_url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.players-cont")))

    # it works! check if player is in squad
    in_squad_ids = set()
    all_links = driver.find_elements(By.CSS_SELECTOR, "div.players-cont a[href*='player_id=']")
    for link in all_links:
        href = urljoin(game_url, link.get_attribute("href"))
        pid = parse_qs(urlparse(href).query).get("player_id", [""])[0]
        if pid:
            in_squad_ids.add(pid)

    # players who were in the squad but did not play:
    # get the bench players
    bench_links = driver.find_elements(By.CSS_SELECTOR, "div.home.Bench a[href*='player_id='], div.guest.Bench a[href*='player_id=']")
    bench_player_ids = set()
    for link in bench_links:
        href = urljoin(game_url, link.get_attribute("href"))
        pid = parse_qs(urlparse(href).query).get("player_id", [""])[0]
        if pid:
            bench_player_ids.add(pid)

    for player_id in team.team_players.keys():
        started = None
        in_squad = True
        subbed_in = None
        subbed_out = None
        subbed_in_min = None
        subbed_out_min = None

        # player is not in squad:
        if player_id not in in_squad_ids:
            in_squad = False
            started = False
            # print(started)
            team.team_players[player_id].add_game(game_id,date,started,in_squad,subbed_in,subbed_out,subbed_in_min,subbed_out_min)
            continue

        # players that in the squad but didn't played:
        if player_id in in_squad_ids and player_id in bench_player_ids:
            in_squad = True
            started = False
            subbed_in = False
            subbed_out = False
            team.team_players[player_id].add_game(game_id,date,started,in_squad,subbed_in,subbed_out,subbed_in_min,subbed_out_min)
            continue
        # ---------------------------------------------------------------------------------------

        player_sel = f'a[href*="player_id={player_id}"]'
        player_a = driver.find_element(By.CSS_SELECTOR, player_sel)
        move_elems = player_a.find_elements(By.CSS_SELECTOR, "span.moves span")
        for move in move_elems:
            cls = move.get_attribute("class") or ""
            text = move.text.strip()
            nums = re.findall(r"\d+", text)
            minute = int(nums[0]) if nums else None
            if "change-down" in cls and minute is not None:
                subbed_out_min = minute  

            elif "change-up" in cls and minute is not None:
                subbed_in_min = minute


        # minutes logic covering all cases and updating bool variables
        if not in_squad:
            started = False 
        # started on bench subbed in and subbed out
        elif subbed_in_min and subbed_out_min:
            subbed_in = True
            subbed_out = True
            started = False
        # started on bench and subbed in
        elif subbed_in_min and not subbed_out_min:
            subbed_in = True
            subbed_out = False
            started = False
        # started, then subbed off
        elif not subbed_in_min and subbed_out_min:
            subbed_in = False
            subbed_out = True
            started = True
        # played full match (started and no substitutions)        
        else:
            subbed_in = False
            subbed_out = False
            started = True

        team.team_players[player_id].add_game(game_id,date,started,in_squad,subbed_in,subbed_out,subbed_in_min,subbed_out_min)
    driver.quit()

