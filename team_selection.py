import json

# load  config.json file
def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# it works!
def choose_option(options, prompt):
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            # if the user entered wrong number:
            else:
                print("תכניס מספר בין 1-4")
        except ValueError:
                print("תכניס מספר בין 1-4")


# choose a team:
def choose_team() -> dict:
    config = load_config()
    clubs_names = list(config["clubs"].keys())
    chosen_club = choose_option(clubs_names,"תבחר מועדון - מספר בין 1-4")
    print(f"\nSelected club: {chosen_club}\n")
    club_id = config['clubs'][chosen_club]['club id']
    club_teams = config['clubs'][chosen_club]['club teams']
    team_names = [team['team name'] for team in club_teams]
    chosen_team = choose_option(team_names,"תבחר קבוצה - מספר בין 1-3")
    team_id = None
    for team in club_teams:
        if team['team name'] == chosen_team:
            team_id = team['team id']
            break
    print(f"\nSelected team: {chosen_team}\n")
    base_team_url = config['base team url']
    team_url = base_team_url.format(team_id=team['team id'])
    team_details = {
        'club name': chosen_club,
        'club id': club_id,
        'team name': chosen_team,
        'team id': team_id,
    }
    return team_details

def get_team_id() -> str:
    team_details = choose_team(load_config())
    return team_details['team id']    

def get_club_id() -> str:
    team_details = choose_team(load_config())
    return team_details['club id']
