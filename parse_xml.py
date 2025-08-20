import xml.etree.ElementTree as ET
import json

# load config from config.xml file
def load_config():
    tree = ET.parse('config.xml')
    root = tree.getroot()
    config = {
        'season id': root.findtext('season_id'),
        'base team url': root.findtext(('base_team_url')),
        'base game url': root.findtext(('base_game_url')),
        'base player url': root.findtext(('base_player_url')),
        'base team games url': root.findtext(('base_team_games_url')),
        'base team_players list url': root.findtext(('base_team_players_list_url')),
        'clubs': {}
    }
    
    for club in root.find('clubs').findall('club'):
        club_name = club.findtext('name')
        club_id = club.findtext('club_id')
        teams = []
        for team in club.find('teams').findall('team'):
            team_name = team.findtext('name')
            team_id = team.findtext('team_id')
            teams.append({'team name': team_name, 'team id': team_id})
        config['clubs'][club_name] = {
            'club id': club_id,
            'club teams': teams
        }
    return config

cfg = load_config()

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)

print(load_config())