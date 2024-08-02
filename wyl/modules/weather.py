import requests
from wyl.modules.helpers import hasKey
from wyl.modules.unit_conversions import celsius_to_fahrenheit, km_to_miles, kmh_to_mph
import os.path

locations_filepath = os.getenv('LOCATIONS_FILEPATH')
terminator = os.getenv('LOCATIONS_CSV_TERMINATOR')
owm_request_url_base = os.getenv('OPENWEATHERMAP_REQUEST_URL_BASE')


def get_weather(lat, lon, requests_session: requests.Session, units='metric'):
    owm_api_key = os.getenv('OPENWEATHERMAP_KEY')
    own_request_uri = f"{owm_request_url_base}?units={units}&lat={lat}&lon={lon}&appid={owm_api_key}"
    r = requests_session.head(own_request_uri)

    if r.status_code == 200:
        r = requests_session.get(own_request_uri)
        return r.json()


def append_location_if_new(query: str, place_id: int, new_csv_line_data: str):
    if place_id is not None and os.path.isfile(locations_filepath):
        with open(locations_filepath) as list_f_r:
            content_lines = list_f_r.readlines()
            found_query = any(line.split(terminator)[0].split("=")[1] == query for line in content_lines)
            if not found_query:
                with open(locations_filepath, "a") as list_f:
                    list_f.write(new_csv_line_data + "\n")
                return True
            found_place_id = any(int(line.split(terminator)[0].split("=")[1]) == place_id for line in content_lines)
            if not found_place_id:
                with open(locations_filepath, "a") as list_f:
                    list_f.write(new_csv_line_data + "\n")
                return True
            else:
                print(f"place_id({place_id}) already in")
                return False

    else:
        with open(locations_filepath, "a") as list_f:
            list_f.write(new_csv_line_data + "\n")
            return True


def weather_location_to_csv_line(query: str, j: dict):
    csv_line_data = ""

    current_place_id = None

    csv_line_data += f"query={query}{terminator}"

    # Add place_id first if it exists
    if "place_id" in j:
        current_place_id = j['place_id']
        csv_line_data += f"place_id={j['place_id']}{terminator}"

    # Add the rest of the keys except place_id
    for key, v in j.items():
        if key == "place_id":
            continue  # Skip since place_id is already added

        if isinstance(v, (int, float)):
            csv_line_data += f"{key}={v}{terminator}"
        elif isinstance(v, str):
            csv_line_data += f"{key}={v}{terminator}"
        elif isinstance(v, list):
            csv_line_data += f"{key}={','.join(v)}{terminator}"
    return current_place_id, csv_line_data


def weather_dict_to_template_str(weather: dict):
    main_weather: dict = weather.get('main') if hasKey(weather, 'main') else {}
    temperature = main_weather.get('temp') if hasKey(main_weather, "temp") else None
    temperature_f = celsius_to_fahrenheit(temperature) if temperature is not None else None
    temperature_feels_like = main_weather.get('feels_like') if hasKey(main_weather, "feels_like") else None
    temperature_feels_like_f = celsius_to_fahrenheit(
        temperature_feels_like) if temperature_feels_like is not None else None
    pressure = main_weather.get('pressure') if hasKey(main_weather, "pressure") else None
    humidity = main_weather.get('humidity') if hasKey(main_weather, "humidity") else None
    visibility = weather.get('visibility') if hasKey(weather, "visibility") else None
    visibility_miles = km_to_miles(visibility) if visibility is not None else None
    wind_dict: dict = weather.get('wind') if hasKey(weather, 'wind') else None
    wind_speed = wind_dict.get('speed') if hasKey(wind_dict, "speed") else None
    wind_speed_mph = kmh_to_mph(wind_speed) if wind_speed is not None else None
    wind_direction_deg = wind_dict.get('deg') if hasKey(wind_dict, 'deg') else None
    weather_icon = ""

    location_name = weather.get('name') if hasKey(weather, "name") else None
    template = f"""{location_name}: {weather_icon} {temperature} °C ({temperature_f} °F). """ \
               f""" Feels like {temperature_feels_like} °C ({temperature_feels_like_f} °F). """ \
               f""" Wind is blowing from {wind_direction_deg} degrees at {wind_speed} km/h """ \
               f"""({wind_speed_mph} mp/h). """ \
               f""" {humidity}% humidity. """ \
               f""" Visibility: {visibility} km ({visibility_miles} miles). """ \
               f""" Air pressure: {pressure} hPa."""
    return template

