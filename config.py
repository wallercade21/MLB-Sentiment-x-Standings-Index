# MLB Team configurations
# Each team has a name, abbreviation, MLB team ID (for standings API),
# and a query object to pass directly to the Infegy API.
# Queries match either the team name OR their official fan hashtag.

SEASON_START = "2024-12-01"  # Winter meetings
DATASET_ID = "ds_gj4u3F40SLa"

def _team_query(name, hashtag):
    """Build an or query matching the team name or their hashtag."""
    return {
        "op": "or",
        "values": [
            {"op": "contains", "field": "body", "value": name},
            {"op": "contains", "field": "body", "value": hashtag}
        ]
    }

TEAMS = [
    # AL East
    {"name": "New York Yankees",     "abbr": "NYY", "mlb_id": 147, "division": "AL East",    "query": _team_query("new york yankees",       "#repbx")},
    {"name": "Boston Red Sox",       "abbr": "BOS", "mlb_id": 111, "division": "AL East",    "query": _team_query("boston red sox",          "#dirtywater")},
    {"name": "Toronto Blue Jays",    "abbr": "TOR", "mlb_id": 141, "division": "AL East",    "query": _team_query("toronto blue jays",       "#nextlevel")},
    {"name": "Tampa Bay Rays",       "abbr": "TB",  "mlb_id": 139, "division": "AL East",    "query": _team_query("tampa bay rays",          "#raysup")},
    {"name": "Baltimore Orioles",    "abbr": "BAL", "mlb_id": 110, "division": "AL East",    "query": _team_query("baltimore orioles",       "#birdland")},
    # AL Central
    {"name": "Cleveland Guardians",  "abbr": "CLE", "mlb_id": 114, "division": "AL Central", "query": _team_query("cleveland guardians",     "#guardsball")},
    {"name": "Minnesota Twins",      "abbr": "MIN", "mlb_id": 142, "division": "AL Central", "query": _team_query("minnesota twins",         "#mntwins")},
    {"name": "Chicago White Sox",    "abbr": "CWS", "mlb_id": 145, "division": "AL Central", "query": _team_query("chicago white sox",       "#whitesox")},
    {"name": "Kansas City Royals",   "abbr": "KC",  "mlb_id": 118, "division": "AL Central", "query": _team_query("kansas city royals",      "#fountainsup")},
    {"name": "Detroit Tigers",       "abbr": "DET", "mlb_id": 116, "division": "AL Central", "query": _team_query("detroit tigers",          "#repdetroit")},
    # AL West
    {"name": "Houston Astros",       "abbr": "HOU", "mlb_id": 117, "division": "AL West",    "query": _team_query("houston astros",          "#builtforthis")},
    {"name": "Seattle Mariners",     "abbr": "SEA", "mlb_id": 136, "division": "AL West",    "query": _team_query("seattle mariners",        "#tridents up")},
    {"name": "Texas Rangers",        "abbr": "TEX", "mlb_id": 140, "division": "AL West",    "query": _team_query("texas rangers",           "#allfortx")},
    {"name": "Los Angeles Angels",   "abbr": "LAA", "mlb_id": 108, "division": "AL West",    "query": _team_query("los angeles angels",      "#repthehalo")},
    {"name": "Oakland Athletics",    "abbr": "OAK", "mlb_id": 133, "division": "AL West",    "query": _team_query("oakland athletics",       "#athletics")},
    # NL East
    {"name": "Atlanta Braves",       "abbr": "ATL", "mlb_id": 144, "division": "NL East",    "query": _team_query("atlanta braves",          "#bravescountry")},
    {"name": "New York Mets",        "abbr": "NYM", "mlb_id": 121, "division": "NL East",    "query": _team_query("new york mets",           "#lgm")},
    {"name": "Philadelphia Phillies","abbr": "PHI", "mlb_id": 143, "division": "NL East",    "query": _team_query("philadelphia phillies",   "#ringthebell")},
    {"name": "Miami Marlins",        "abbr": "MIA", "mlb_id": 146, "division": "NL East",    "query": _team_query("miami marlins",           "#marlinsbeisbol")},
    {"name": "Washington Nationals", "abbr": "WSH", "mlb_id": 120, "division": "NL East",    "query": _team_query("washington nationals",    "#natitude")},
    # NL Central
    {"name": "Milwaukee Brewers",    "abbr": "MIL", "mlb_id": 158, "division": "NL Central", "query": _team_query("milwaukee brewers",       "#thisismycrew")},
    {"name": "Chicago Cubs",         "abbr": "CHC", "mlb_id": 112, "division": "NL Central", "query": _team_query("chicago cubs",            "#behereforit")},
    {"name": "Cincinnati Reds",      "abbr": "CIN", "mlb_id": 113, "division": "NL Central", "query": _team_query("cincinnati reds",         "#atobttr")},
    {"name": "Pittsburgh Pirates",   "abbr": "PIT", "mlb_id": 134, "division": "NL Central", "query": _team_query("pittsburgh pirates",      "#letsgobucs")},
    {"name": "St. Louis Cardinals",  "abbr": "STL", "mlb_id": 138, "division": "NL Central", "query": _team_query("st louis cardinals",      "#forthelou")},
    # NL West
    {"name": "Los Angeles Dodgers",  "abbr": "LAD", "mlb_id": 119, "division": "NL West",    "query": _team_query("los angeles dodgers",     "#letsgododgers")},
    {"name": "San Francisco Giants", "abbr": "SF",  "mlb_id": 137, "division": "NL West",    "query": _team_query("san francisco giants",    "#sfgiants")},
    {"name": "San Diego Padres",     "abbr": "SD",  "mlb_id": 135, "division": "NL West",    "query": _team_query("san diego padres",        "#forthefaithful")},
    {"name": "Arizona Diamondbacks", "abbr": "ARI", "mlb_id": 109, "division": "NL West",    "query": _team_query("arizona diamondbacks",   "#dbacks")},
    {"name": "Colorado Rockies",     "abbr": "COL", "mlb_id": 115, "division": "NL West",    "query": _team_query("colorado rockies",        "#rockies")},
]

# Build a lookup dict by mlb_id for easy merging later
TEAM_BY_MLB_ID = {t["mlb_id"]: t for t in TEAMS}
