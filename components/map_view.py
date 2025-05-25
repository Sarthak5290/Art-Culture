import streamlit as st
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()


def get_nearby_places(lat, lng, radius=1000):
    """Get nearby famous places using Google Places API."""
    try:
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": "tourist_attraction|landmark|museum|art_gallery",
            "key": os.getenv("GOOGLE_MAPS_API_KEY"),
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] != "OK":
            return []

        places = []
        for place in data.get("results", [])[:2]:  # Get top 2 nearby places
            location = place["geometry"]["location"]
            places.append(
                {"name": place["name"], "lat": location["lat"], "lng": location["lng"]}
            )
        return places
    except Exception:
        return []


def get_street_view_urls(location):
    """Get street view URLs for a location and nearby famous places."""
    try:
        # Set loading state
        st.session_state.map_loading = True

        # Get coordinates using Google Geocoding API
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": location, "key": os.getenv("GOOGLE_MAPS_API_KEY")}
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] != "OK":
            st.session_state.map_loading = False
            return []

        # Get main location
        main_location = data["results"][0]["geometry"]["location"]
        urls = []

        # Add main location
        main_url = f"https://www.google.com/maps/embed/v1/streetview?key={os.getenv('GOOGLE_MAPS_API_KEY')}&location={main_location['lat']},{main_location['lng']}"
        urls.append({"url": main_url, "title": "Main Location"})

        # Get nearby famous places
        nearby_places = get_nearby_places(main_location["lat"], main_location["lng"])
        for place in nearby_places:
            url = f"https://www.google.com/maps/embed/v1/streetview?key={os.getenv('GOOGLE_MAPS_API_KEY')}&location={place['lat']},{place['lng']}"
            urls.append({"url": url, "title": place["name"]})

        # Clear loading state
        st.session_state.map_loading = False
        return urls
    except Exception:
        st.session_state.map_loading = False
        return []


def render_street_view(location):
    """Render street view iframes for a location."""
    if not location:
        return

    urls = get_street_view_urls(location)
    if not urls:
        st.error("Could not find location on Google Maps")
        return

    # Create columns for the street view iframes
    cols = st.columns(len(urls))

    for i, view_data in enumerate(urls):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background: var(--card-bg);
                    padding: 1rem;
                    border-radius: 10px;
                    border: 1px solid var(--border-color);
                    margin-bottom: 1rem;
                ">
                    <h4 style="
                        color: var(--text-light);
                        margin: 0 0 0.8rem 0;
                        font-size: 1rem;
                        text-align: center;
                    ">{view_data['title']}</h4>
                    <iframe
                        width="100%"
                        height="300"
                        frameborder="0"
                        style="border:0"
                        src="{view_data['url']}"
                        allowfullscreen>
                    </iframe>
                </div>
                """,
                unsafe_allow_html=True,
            )
