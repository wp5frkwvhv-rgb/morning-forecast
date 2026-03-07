#!/usr/bin/env python3
"""
Morning Forecast Texter — Single-file SMS weather app.
Setup: pip install requests twilio
Run:   python morning_forecast.py
"""

import os, sys, logging, requests
from twilio.rest import Client as TwilioClient

# ===== CONFIG (set via environment variables or GitHub Secrets) =====
TWILIO_SID   = os.getenv("TWILIO_ACCOUNT_SID",  "YOUR_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN",    "YOUR_AUTH_TOKEN")
TWILIO_FROM  = os.getenv("TWILIO_PHONE_NUMBER",  "+17853011564")
MY_PHONE     = os.getenv("MY_PHONE_NUMBER",       "+12147272250")
AMBEE_KEY    = os.getenv("AMBEE_API_KEY",          "")

NAME     = "Chris"
LOCATION = "McKinney"
LAT      = 33.1974
LON      = -96.6153
# ====================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# WMO weather code -> (description, emoji)
WMO = {
    0: ("Clear Sky","☀️"), 1: ("Mostly Clear","🌤️"), 2: ("Partly Cloudy","⛅"),
    3: ("Overcast","☁️"), 45: ("Foggy","🌫️"), 48: ("Icy Fog","🌫️"),
    51: ("Light Drizzle","🌦️"), 53: ("Drizzle","🌦️"), 55: ("Heavy Drizzle","🌧️"),
    56: ("Freezing Drizzle","🌧️"), 57: ("Heavy Freezing Drizzle","🌧️"),
    61: ("Light Rain","🌦️"), 63: ("Rain","🌧️"), 65: ("Heavy Rain","🌧️"),
    66: ("Freezing Rain","🧊"), 67: ("Heavy Freezing Rain","🧊"),
    71: ("Light Snow","🌨️"), 73: ("Snow","❄️"), 75: ("Heavy Snow","❄️"),
    77: ("Snow Grains","❄️"), 80: ("Light Showers","🌦️"), 81: ("Showers","🌧️"),
    82: ("Heavy Showers","🌧️"), 85: ("Light Snow Showers","🌨️"),
    86: ("Heavy Snow Showers","🌨️"), 95: ("Thunderstorm","⛈️"),
    96: ("Thunderstorm + Hail","⛈️"), 99: ("Severe Thunderstorm","⛈️"),
}

def c_to_f(c): return round(c * 9 / 5 + 32)

def get_weather():
    log.info("Fetching weather...")
    r = requests.get("https://api.open-meteo.com/v1/forecast", timeout=15, params={
        "latitude": LAT, "longitude": LON, "forecast_days": 1,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "America/Chicago",
    }).json()["daily"]
    code = int(r["weather_code"][0])
    desc, emoji = WMO.get(code, ("Unknown","🌡️"))
    return {"high": c_to_f(r["temperature_2m_max"][0]), "low": c_to_f(r["temperature_2m_min"][0]),
            "rain": int(r["precipitation_probability_max"][0] or 0), "desc": desc, "emoji": emoji}

def get_pollen():
    if not AMBEE_KEY: return None
    log.info("Fetching pollen...")
    data = requests.get("https://api.ambeedata.com/latest/pollen/by-lat-lng", timeout=15,
        params={"lat": LAT, "lng": LON}, headers={"x-api-key": AMBEE_KEY}).json()
    risk = data.get("data",[{}])[0].get("Risk",{})
    levels = {"Low":1,"Moderate":2,"High":3,"Very High":4}
    best = max((risk.get(k,"Low") for k in ["tree_pollen","grass_pollen","weed_pollen"]),
               key=lambda v: levels.get(v,0))
    return {"overall": best, "tree": risk.get("tree_pollen","Low"), "grass": risk.get("grass_pollen","Low")}

def main():
    if "YOUR_" in TWILIO_SID or "YOUR_" in TWILIO_TOKEN:
        log.error("Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables.")
        sys.exit(1)

    try:    w = get_weather()
    except: w = {"high":"??","low":"??","rain":"?","desc":"unavailable","emoji":"🌡️"}

    try:    p = get_pollen()
    except: p = None

    msg = f"Good morning {NAME}! 🌅\n{LOCATION}: {w['high']}°F/{w['low']}°F, {w['desc']} {w['emoji']}, {w['rain']}% rain."
    if p: msg += f"\nPollen: {p['overall']} (Tree:{p['tree']}, Grass:{p['grass']})."
    msg += "\nHave a great day! 💪"
    if len(msg) > 280: msg = msg[:277] + "..."

    log.info("SMS (%d chars):\n%s", len(msg), msg)
    try:
        sid = TwilioClient(TWILIO_SID, TWILIO_TOKEN).messages.create(body=msg, from_=TWILIO_FROM, to=MY_PHONE).sid
        log.info("Sent — SID: %s", sid)
    except Exception as e:
        log.error("Send failed: %s", e)
        try: TwilioClient(TWILIO_SID, TWILIO_TOKEN).messages.create(
                body=f"Good morning {NAME}! Forecast unavailable — check your weather app. 💪",
                from_=TWILIO_FROM, to=MY_PHONE)
        except: sys.exit(1)

if __name__ == "__main__":
    main()
