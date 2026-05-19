import yfinance as yf
import random
import streamlit as st
import folium
import requests
import feedparser
import pandas as pd

from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(layout="wide")

st.title("🌍 Global Intelligence Monitor")

# ---------------- SIDEBAR ----------------

st.sidebar.header("GLOBAL SITUATION")

earthquakes = st.sidebar.checkbox("🌋 Earthquakes", True)
conflicts = st.sidebar.checkbox("⚔ Conflict Zones", True)
bases = st.sidebar.checkbox("🛡 Military Bases", True)
nuclear = st.sidebar.checkbox("☢ Nuclear Sites", True)
aircraft = st.sidebar.checkbox("✈ Aircraft", True)
wildfires = st.sidebar.checkbox("🔥 Wildfires", True)
storms = st.sidebar.checkbox("🌪 Storm Systems", True)
clouds = st.sidebar.checkbox("☁ Satellite Clouds", True)

# ---------------- MAP ----------------

m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB dark_matter")

# ---------------- SATELLITE CLOUDS ----------------

if clouds:

    folium.TileLayer(
        tiles="https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=439d4b804bc8187953eb36d2a8c26a02",
        attr="OpenWeather",
        name="Clouds",
        overlay=True
    ).add_to(m)

# ---------------- EARTHQUAKES ----------------

if earthquakes:

    try:

        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        data = requests.get(url).json()

        heat = []

        for eq in data["features"]:

            lon = eq["geometry"]["coordinates"][0]
            lat = eq["geometry"]["coordinates"][1]
            mag = eq["properties"]["mag"]

            if mag:

                heat.append([lat,lon])

                color = "yellow"

                if mag >= 6:
                    color = "red"
                elif mag >= 4:
                    color = "orange"

                folium.CircleMarker(
                    [lat,lon],
                    radius=2+mag,
                    color=color,
                    fill=True,
                    popup=f"M {mag}"
                ).add_to(m)

        HeatMap(heat,radius=15).add_to(m)

    except:
        pass

# ---------------- CONFLICT ZONES ----------------

if conflicts:

    zones = [
        (48,34,"Ukraine War"),
        (31,35,"Israel Conflict"),
        (15,30,"Sudan War"),
        (21,96,"Myanmar Conflict")
    ]

    for lat,lon,name in zones:

        folium.Circle(
            [lat,lon],
            radius=600000,
            color="red",
            fill=True,
            fill_opacity=0.2,
            popup=name
        ).add_to(m)

# ---------------- MILITARY BASES ----------------

if bases:

    base_list = [

        (49.4,7.6,"Ramstein"),
        (21.3,-157.8,"Pearl Harbor"),
        (-7.3,72.4,"Diego Garcia"),
        (35.7,139.7,"Tokyo Base"),
        (28.6,77.2,"Delhi Base")

    ]

    for lat,lon,name in base_list:

        folium.Marker(
            [lat,lon],
            icon=folium.Icon(color="green",icon="flag"),
            popup=name
        ).add_to(m)

# ---------------- NUCLEAR SITES ----------------

if nuclear:

    plants = [

        (51.2767,30.2219,"Chernobyl"),
        (37.421,141.032,"Fukushima"),
        (40.153,-76.724,"Three Mile Island")

    ]

    for lat,lon,name in plants:

        folium.Marker(
            [lat,lon],
            icon=folium.Icon(color="purple",icon="bolt"),
            popup=name
        ).add_to(m)

# ---------------- AIRCRAFT ----------------

if aircraft:

    planes = [

        (51.47,-0.45,"BAW123"),
        (40.64,-73.78,"DAL456"),
        (35.55,139.78,"ANA789"),
        (25.25,55.36,"UAE202")

    ]

    for lat,lon,name in planes:

        folium.CircleMarker(
            [lat,lon],
            radius=4,
            color="cyan",
            fill=True,
            popup=name
        ).add_to(m)
    
# ---------------- SATELLITES ----------------

satellites = st.sidebar.checkbox("🛰 Satellites", True)

if satellites:

    # Example satellites

    sat_data = [

        (0,0,"ISS"),
        (10,30,"Starlink"),
        (-20,120,"Starlink"),
        (40,-60,"Starlink")

    ]

    for lat,lon,name in sat_data:

        folium.CircleMarker(
            [lat,lon],
            radius=4,
            color="white",
            fill=True,
            popup=name
        ).add_to(m)

# ---------------- SHIPS ----------------

ships = st.sidebar.checkbox("🚢 Ships", True)

if ships:

    ship_data = [

        (25,55,"Cargo Ship"),
        (35,140,"Container Ship"),
        (40,-20,"Oil Tanker"),
        (-10,110,"Freighter")

    ]

    for lat,lon,name in ship_data:

        folium.CircleMarker(
            [lat,lon],
            radius=4,
            color="blue",
            fill=True,
            popup=name
        ).add_to(m)

# ---------------- NASA WILDFIRES ----------------

if wildfires:

    try:

        url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/text/MODIS_C6_Global_24h.csv"

        df = pd.read_csv(url)

        for _,row in df.head(300).iterrows():

            folium.CircleMarker(
                [row["latitude"],row["longitude"]],
                radius=4,
                color="yellow",
                fill=True,
                popup="Wildfire detection"
            ).add_to(m)

    except:
        pass

# ---------------- STORMS ----------------

if storms:

    storms_data = [

        (15,-60,"Atlantic Storm"),
        (20,120,"Pacific Storm"),
        (-12,160,"Pacific Cyclone")

    ]

    for lat,lon,name in storms_data:

        folium.Circle(
            [lat,lon],
            radius=800000,
            color="blue",
            fill=True,
            fill_opacity=0.15,
            popup=name
        ).add_to(m)

# ---------------- SHOW MAP ----------------

st_folium(m,width=1300,height=650)

st.subheader("📈 Global Economic Indicators")

try:

    sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1]
    oil = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]
    gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]

    col1,col2,col3 = st.columns(3)

    col1.metric("S&P 500", round(sp500,2))
    col2.metric("Oil Price", round(oil,2))
    col3.metric("Gold Price", round(gold,2))

except:

    st.write("Economic data unavailable")

# ---------------- NEWS ----------------

st.subheader("📰 Global News Intelligence")

import feedparser

sources = {

"Reuters": "https://www.reuters.com/world/rss",
"BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
"NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
"Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml"

}

search = st.text_input("Search news")

articles = []

for source, url in sources.items():

    feed = feedparser.parse(url)

    for entry in feed.entries[:5]:

        title = entry.title
        link = entry.link

        articles.append({
            "title": title,
            "link": link,
            "source": source
        })

# filtering

if search:

    articles = [
        a for a in articles
        if search.lower() in a["title"].lower()
    ]

# show articles

for article in articles:

    title = article["title"]

    tag = ""

    t = title.lower()

    if "war" in t or "conflict" in t:
        tag = "⚔ Conflict"

    elif "economy" in t or "market" in t:
        tag = "📈 Economy"

    elif "storm" in t or "earthquake" in t:
        tag = "🌪 Disaster"

    elif "tech" in t:
        tag = "💻 Tech"

    st.markdown(
        f"""
        **{tag} [{title}]({article['link']})**  
        Source: *{article['source']}*
        """
    )

st.subheader("🤖 Global Situation Summary")

summary = random.choice([

"Moderate global instability with multiple regional conflicts and elevated earthquake activity.",

"Increased wildfire detections and storm systems developing in the Pacific region.",

"Global conditions stable with localized geopolitical tensions.",

"Elevated activity detected across multiple monitoring layers."

])

st.write(summary)