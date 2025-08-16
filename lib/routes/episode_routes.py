from flask import Blueprint, jsonify, request
from lib.controller.Episode_Controller import Episode_Controller

episode_bp = Blueprint('episode', __name__, url_prefix='/episode')

@episode_bp.route('/')

def get_episodes() -> jsonify:
   return jsonify(Episode_Controller.get_all_episode_metadata())

@episode_bp.route('/clear')

def clear_catalog() -> str:
   Episode_Controller.delete_all_episode_metadata()
   return '', 200