import requests
import pytz
import csv
from datetime import datetime
from geopy.geocoders import Nominatim

LOG_FILE = 'log.csv'

def log_user_activity(email, action, sunrise=None, sunset=None, solar_noon=None, day_length=None, login_time=None, logout_time=None, session_duration=None):
    """Log user activity to a CSV file."""
    with open(LOG_FILE, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        if action == 'login':
            writer.writerow([email, action, login_time, sunrise, sunset, solar_noon, day_length, ''])
        elif action == 'logout':
            writer.writerow([email, action, logout_time, '', '', '', '', session_duration])

def get_location_from_city(city):
    """Get latitude and longitude from a city name."""
    try:
        geolocator = Nominatim(user_agent="sunrise_sunset_app")
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error getting location: {e}")
        return None, None

def convert_utc_to_local(utc_time_str, timezone_str):
    """Convert UTC time to local time based on timezone."""
    try:
        utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        local_tz = pytz.timezone(timezone_str)
        local_time = utc_time.astimezone(local_tz)
        return local_time.strftime('%Y-%m-%d %I:%M:%S %p')
    except Exception as e:
        print(f"Error converting time: {e}")
        return utc_time_str

def get_timezone_from_lat_long(lat, lng):
    """Get timezone from latitude and longitude."""
    try:
        response = requests.get(f"http://api.geonames.org/timezoneJSON?lat={lat}&lng={lng}&username=faizan_123")
        data = response.json()
        timezone = data.get('timezoneId', 'Asia/Kolkata')
        return timezone
    except requests.exceptions.RequestException as e:
        print(f"Error fetching timezone: {e}")
        return 'Asia/Kolkata'

def get_sunrise_sunset(city, email, login_time):
    """Get sunrise and sunset times for a specified city."""
    latitude, longitude = get_location_from_city(city)
    if not latitude or not longitude:
        print("Invalid location.")
        return None, None, None, None

    api_url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data['status'] == "OK":
            sunrise_utc = data['results']['sunrise']
            sunset_utc = data['results']['sunset']
            solar_noon_utc = data['results']['solar_noon']
            day_length = int(data['results']['day_length'])  # Convert seconds to minutes
            
            day_length_hours = day_length // 3600
            day_length_minutes = (day_length % 3600) // 60

            timezone = get_timezone_from_lat_long(latitude, longitude)
            
            # Convert times from UTC to local
            sunrise_local = convert_utc_to_local(sunrise_utc, timezone)
            sunset_local = convert_utc_to_local(sunset_utc, timezone)
            solar_noon_local = convert_utc_to_local(solar_noon_utc, timezone)
            
            return sunrise_local, sunset_local, solar_noon_local, (day_length_hours, day_length_minutes)
        else:
            print("Error in API response:", data.get('message', ''))
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sunrise and sunset data: {e}")
        return None, None, None, None
