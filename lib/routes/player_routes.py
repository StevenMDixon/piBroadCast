from flask import Blueprint, jsonify, request
import subprocess
import sys

player_bp = Blueprint('player', __name__, url_prefix='/player')

process = None

@player_bp.route('/start')

def start_player():
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen([sys.executable, "player_sub.py"])
        return 'Running Player'
    else:
        return 'Player is already playing'
    
@player_bp.route('/status')

def get_player_status():
    pass

@player_bp.route('/kill')

def kill_player():
    global process
    if process is not None:
        process = process.terminate()
        return "Player terminated"
    else:
        return 'No player found to terminate'