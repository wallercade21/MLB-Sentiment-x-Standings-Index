import requests
from datetime import datetime, timedelta

MLB_BASE = "https://statsapi.mlb.com/api/v1"
LEAGUE_IDS = "103,104"  # 103 = AL, 104 = NL
SEASON = "2026"


def get_current_standings():
    """
    Fetches current MLB standings from the free MLB Stats API.
    Returns a dict keyed by team MLB ID:
    {
      147: {"wins": 40, "losses": 25, "win_pct": 0.615, "games_back": 0.0},
      ...
    }
    """
    url = f"{MLB_BASE}/standings"
    params = {
        "leagueId": LEAGUE_IDS,
        "season": SEASON,
        "standingsTypes": "regularSeason"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    standings = {}
    for division in data.get("records", []):
        for team_rec in division.get("teamRecords", []):
            team_id = team_rec["team"]["id"]
            wins = team_rec["wins"]
            losses = team_rec["losses"]
            total = wins + losses
            win_pct = round(wins / total, 3) if total > 0 else 0.0
            standings[team_id] = {
                "wins": wins,
                "losses": losses,
                "win_pct": win_pct,
                "games_back": team_rec.get("gamesBack", "-"),
                "division": division.get("division", {}).get("name", "")
            }
    return standings


def get_historical_standings(num_weeks=16):
    """
    Fetches standings at weekly intervals going back num_weeks from today.
    Returns a list of { "date": "YYYY-MM-DD", "standings": { team_id: win_pct } }
    sorted oldest to newest. Used for the team detail historical chart.
    """
    results = []
    today = datetime.today()

    # Build list of weekly dates going back num_weeks
    dates = []
    for i in range(num_weeks, -1, -1):
        d = today - timedelta(weeks=i)
        # Don't go before opening day 2026
        if d < datetime(2026, 3, 27):
            continue
        dates.append(d.strftime("%Y-%m-%d"))

    for date_str in dates:
        url = f"{MLB_BASE}/standings"
        params = {
            "leagueId": LEAGUE_IDS,
            "season": SEASON,
            "standingsTypes": "regularSeason",
            "date": date_str
        }
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()

            snapshot = {}
            for division in data.get("records", []):
                for team_rec in division.get("teamRecords", []):
                    team_id = team_rec["team"]["id"]
                    wins = team_rec["wins"]
                    losses = team_rec["losses"]
                    total = wins + losses
                    snapshot[team_id] = round(wins / total, 3) if total > 0 else 0.0

            results.append({"date": date_str, "standings": snapshot})
        except Exception:
            # Skip dates that fail (e.g. before season started)
            continue

    return results
