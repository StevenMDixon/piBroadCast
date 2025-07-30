from flask import Blueprint, jsonify, request
from lib.DataBase import DataBase
import json

station_bp = Blueprint('station', __name__, url_prefix='/station')

current_station_info =  {
            "station_name": "kwb",
            "subtitles": True,
            "playlist_location": "./playlists/",
            "station_src": "",
            "start_time": -1 
    }

@station_bp.route('/')

def get_station_info():
    global current_station_info
    print(current_station_info)
    # need to load this from station_setting file?
    return json.dumps(current_station_info, indent=4)

@station_bp.route('/set', methods=['POST'])

def set_station_info():
    global current_station_info
    print(request.json)
    current_station_info["station_src"] = request.json["station_src"]
    return jsonify(isError= False,
            message= "Success",
            statusCode= 200,
            data= ""), 200
