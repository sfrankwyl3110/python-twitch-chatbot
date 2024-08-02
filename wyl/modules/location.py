import os
import requests


def get_lat_lon(city: str, requests_session: requests.Session):
    nominatim_hostport = os.getenv('NOMINATIM_HOSTPORT')
    request_url = f'http://{nominatim_hostport}/search?q={city}'
    r = requests_session.head(request_url)
    if r.status_code == 200:
        r = requests_session.get(request_url)
        return r.json()
    return {}
