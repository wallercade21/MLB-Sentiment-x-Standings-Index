import os
import requests
from config import DATASET_ID, SEASON_START, TEAMS

STARSCAPE_BASE = "https://starscape.infegy.com/api"

def get_headers():
    token = os.getenv("STARSCAPE_TOKEN")
    if not token:
        print("ERROR: STARSCAPE_TOKEN is missing from environment variables")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# Exclude replies and shares from all queries
EXCLUDE_REPLIES_AND_SHARES = {
    "op": "not",
    "values": [
        {
            "op": "contains",
            "fields": ["is_reply_or_share"],
            "values": ["1", "2"]
        }
    ]
}


def get_team_sentiment(team):
    """
    Runs a sentiment keyword agg for a single team since SEASON_START.
    Returns raw counts and a sentiment ratio score (positive / total non-neutral).

    Sentiment ratio is calculated as:
      positive / (positive + negative)
    This gives a 0-1 score where 0.5 is perfectly balanced,
    above 0.5 is net positive, below 0.5 is net negative.
    """
    payload = {
        "dataset_id": DATASET_ID,
        "query": {
            "op": "and",
            "values": [
                team["query"],
                {
                    "op": "range",
                    "field": "published",
                    "lower": SEASON_START,
                    "upper": "now"
                },
                EXCLUDE_REPLIES_AND_SHARES
            ]
        },
        "aggs": {
            "sentiment": {
                "op": "keyword",
                "field": "sentiment",
                "include_null": False
            }
        }
    }

    try:
        r = requests.post(
            f"{STARSCAPE_BASE}/query/agg?include_total=true",
            json=payload,
            headers=get_headers(),
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        total = data.get("_total", 0)
        buckets = data.get("sentiment", {}).get("_buckets", [])
        counts = {b["_key"]: b["_count"] for b in buckets}

        positive = counts.get("p", 0)
        negative = counts.get("n", 0)
        neutral  = counts.get("0", 0)
        scored   = positive + negative

        sentiment_ratio = round(positive / scored, 3) if scored > 0 else 0.5
        positive_pct    = round(positive / total * 100, 1) if total > 0 else 0
        negative_pct    = round(negative / total * 100, 1) if total > 0 else 0
        neutral_pct     = round(neutral  / total * 100, 1) if total > 0 else 0

        return {
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "sentiment_ratio": sentiment_ratio,
            "positive_pct": positive_pct,
            "negative_pct": negative_pct,
            "neutral_pct": neutral_pct,
            "error": None
        }

    except Exception as e:
        print(f"  ERROR fetching sentiment for {team.get('name', '?')}: {e}")
        return {
            "total": 0, "positive": 0, "negative": 0, "neutral": 0,
            "sentiment_ratio": 0.5, "positive_pct": 0,
            "negative_pct": 0, "neutral_pct": 0,
            "error": str(e)
        }


def get_all_team_sentiments():
    """
    Runs sentiment queries for all 30 teams sequentially.
    Returns a list of team dicts merged with sentiment results.
    """
    results = []
    for team in TEAMS:
        print(f"  Querying {team['name']}...")
        sentiment = get_team_sentiment(team)
        results.append({**team, **sentiment})
    return results


def get_team_sentiment_history(team):
    """
    Runs a weekly histogram with sentiment sub-agg for a single team
    going back to SEASON_START. Used for the team detail page.
    Returns a list of { date, positive, negative, neutral, sentiment_ratio }
    """
    payload = {
        "dataset_id": DATASET_ID,
        "query": {
            "op": "and",
            "values": [
                team["query"],
                {
                    "op": "range",
                    "field": "published",
                    "lower": SEASON_START,
                    "upper": "now"
                },
                EXCLUDE_REPLIES_AND_SHARES
            ]
        },
        "aggs": {
            "weekly": {
                "op": "histogram",
                "field": "published",
                "interval": "week",
                "aggs": {
                    "sentiment": {
                        "op": "keyword",
                        "field": "sentiment"
                    }
                }
            }
        }
    }

    try:
        r = requests.post(
            f"{STARSCAPE_BASE}/query/agg",
            json=payload,
            headers=get_headers(),
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        history = []
        for bucket in data.get("weekly", {}).get("_buckets", []):
            counts = {b["_key"]: b["_count"] for b in bucket.get("sentiment", {}).get("_buckets", [])}
            positive = counts.get("p", 0)
            negative = counts.get("n", 0)
            neutral  = counts.get("0", 0)
            scored   = positive + negative
            ratio    = round(positive / scored, 3) if scored > 0 else 0.5

            history.append({
                "date": bucket.get("_label", ""),
                "positive": positive,
                "negative": negative,
                "neutral": neutral,
                "sentiment_ratio": ratio
            })

        return history

    except Exception as e:
        return []
