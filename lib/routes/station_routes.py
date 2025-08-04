from flask import Blueprint, jsonify, request
from lib.controller.Station_Controller import Station_Controller
from lib.models.dto import StationConfig
import json

station_bp = Blueprint('station', __name__, url_prefix='/station')

# def load_station_config(configPath):
#     try:
#         with open(configPath, 'r') as file:
#             # Load the JSON data from the file into a Python dictionary or list
#             return json.load(file)
#     except:
#         return  {
#             "station_name": "default_station",
#             "subtitles": False,
#             "playlist_location": "./playlists/",
#             "playlist_file": "",
#             "start_time": -1 
#         }

# current_station_info = load_station_config("./template/settings.json")

@station_bp.route('/')

def get_station_info():
    station_config_data = Station_Controller.get_current_station_config()
    station_config = StationConfig(*station_config_data) if station_config_data != None else None
    return jsonify(station_config)

@station_bp.route('/set', methods=['POST'])

def set_station_info():
    station_config_data = request.json
    station_config = StationConfig(**station_config_data)

    Station_Controller.add_station_config(station_config)
    return "New Station config set", 200


