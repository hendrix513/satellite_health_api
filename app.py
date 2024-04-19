import datetime
from datetime import timedelta
import logging

from flask import Flask, jsonify, current_app
import requests
import pandas as pd

import threading

from flask import Blueprint
route_blueprint = Blueprint('route_blueprint', __name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


satellite_data_url = "http://nestio.space/api/satellite/data"
data_history = pd.DataFrame(columns=["time", "altitude"])


def create_app():
    threading.Thread(target=fetch_satellite_data, daemon=True).start()

    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    app.register_blueprint(route_blueprint)

    return app


def fetch_satellite_data():
    logger = logging.getLogger(__name__)
    while True:
        try:
            new_data = requests.get(satellite_data_url).json()
            ts = datetime.datetime.fromisoformat(new_data["last_updated"]).astimezone(datetime.timezone.utc).timestamp()
            data_history.loc[len(data_history.index)] = [ts, float(new_data["altitude"])]
        except Exception as e:
            logger.error(f"Failed to fetch satellite data: {e}")
        # Wait for 10 seconds before fetching data again
        threading.Event().wait(10)


def _get_current_timestamp():
    return datetime.datetime.timestamp(datetime.datetime.now(datetime.UTC))


def get_data_history(num_minutes):
    ts = _get_current_timestamp() - 60 * num_minutes
    ret = data_history.loc[data_history.time > ts, 'altitude'].tolist()
    return ret


def check_health():
    altitudes = get_data_history(1)
    if not altitudes:
        return "No data available"
    avg_altitude_last_minute = sum(altitudes)/ len(altitudes)

    if avg_altitude_last_minute < 160:
        return "WARNING: RAPID ORBITAL DECAY IMMINENT"
    elif 160 <= avg_altitude_last_minute < 180:
        return "Sustained Low Earth Orbit Resumed"
    else:
        return "Altitude is A-OK"


@route_blueprint.route('/stats')
def get_stats():
    altitudes = get_data_history(5)
    res = {
        "min_altitude": min(altitudes),
        "max_altitude": max(altitudes),
        "avg_altitude": sum(altitudes)/len(altitudes)
    } if altitudes else {}

    return jsonify(res)


@route_blueprint.route('/health')
def get_health():
    return jsonify({"message": check_health()})
