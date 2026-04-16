import os
from flask import Flask, render_template, jsonify
from flask_caching import Cache
from dotenv import load_dotenv
from config import TEAMS, TEAM_BY_MLB_ID
from mlb_api import get_current_standings, get_historical_standings
from infegy_api import get_all_team_sentiments, get_team_sentiment_history

load_dotenv()

app = Flask(__name__)

# Cache results in memory for 15 minutes so repeated visits don't re-fire all API calls
cache = Cache(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 900  # 15 minutes
})


def build_dashboard_data():
    """
    Fetches standings + sentiment for all 30 teams and merges them.
    Called once on page load of the main dashboard.
    """
    print("Fetching MLB standings...")
    standings = get_current_standings()

    print("Fetching sentiment for all teams (sequential)...")
    sentiment_data = get_all_team_sentiments()

    # Merge standings into sentiment results
    merged = []
    for team in sentiment_data:
        mlb_id = team["mlb_id"]
        s = standings.get(mlb_id, {})
        merged.append({
            **team,
            "wins":     s.get("wins", 0),
            "losses":   s.get("losses", 0),
            "win_pct":  s.get("win_pct", 0.0),
            "games_back": s.get("games_back", "-"),
        })

    # Sort by sentiment ratio descending for the leaderboard
    merged.sort(key=lambda x: x["sentiment_ratio"], reverse=True)
    for i, team in enumerate(merged):
        team["sentiment_rank"] = i + 1

    return merged


# --- Routes ---

@app.route("/")
@cache.cached(timeout=900, key_prefix="dashboard")
def index():
    """Main dashboard — fetches all data and renders scatter + table."""
    data = build_dashboard_data()
    return render_template("index.html", teams=data)


@app.route("/team/<abbr>")
@cache.cached(timeout=900, key_prefix=lambda: f"team_{__import__('flask').request.view_args['abbr']}")
def team_detail(abbr):
    """
    Team detail page — shows historical sentiment vs win% over time.
    Looks up the team by abbreviation, then fetches historical data.
    """
    team = next((t for t in TEAMS if t["abbr"] == abbr), None)
    if not team:
        return "Team not found", 404

    print(f"Fetching sentiment history for {team['name']}...")
    sentiment_history = get_team_sentiment_history(team)

    print("Fetching historical standings...")
    standings_history = get_historical_standings(num_weeks=16)

    # Build aligned time series for the chart
    mlb_id = team["mlb_id"]
    standings_by_date = {s["date"]: s["standings"].get(mlb_id, None) for s in standings_history}

    chart_labels = []
    sentiment_series = []
    win_pct_series = []
    standings_dates = sorted(standings_by_date.keys())

    for week in sentiment_history:
        label = week["date"]
        chart_labels.append(label)
        sentiment_series.append(week["sentiment_ratio"])

        closest = min(standings_dates, key=lambda d: abs(d - label) if d >= label else float("inf"), default=None)
        win_pct = standings_by_date.get(closest) if closest else None
        win_pct_series.append(win_pct)

    return render_template("team.html",
        team=team,
        chart_labels=chart_labels,
        sentiment_series=sentiment_series,
        win_pct_series=win_pct_series,
        sentiment_history=sentiment_history
    )


if __name__ == "__main__":
    app.run(debug=True)
