# plugins/location_manager.py

from geopy.geocoders import Nominatim
import geocoder
import time

geolocator = Nominatim(user_agent="tezus_location")

def get_coordinates() -> dict:
    """
    Returns current latitude and longitude using IP-based geolocation.
    """
    g = geocoder.ip('me')
    if g.ok:
        return {"latitude": g.latlng[0], "longitude": g.latlng[1]}
    else:
        return {"error": "Unable to detect location"}

def get_address(lat: float, lon: float) -> str:
    """
    Returns human-readable address from coordinates.
    """
    time.sleep(1)  # Respect Nominatim usage policy
    location = geolocator.reverse((lat, lon), language="en")
    return location.address if location else "Address not found"

def get_location() -> str:
    """
    Combines coordinate detection and reverse geocoding.
    """
    coords = get_coordinates()
    if "error" in coords:
        return coords["error"]

    address = get_address(coords["latitude"], coords["longitude"])
    return f"📍 You are at:\n{address}\n({coords['latitude']}, {coords['longitude']})"
