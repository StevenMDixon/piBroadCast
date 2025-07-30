from flask import Blueprint, jsonify, request
from lib.DataBase import DataBase

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@schedule_bp.route('/')

def get_schedule():
    return DataBase.get_schedules()

@schedule_bp.route('/today', methods=['GET'])

def get_todays_schedule():
    return DataBase.get_today_schedules()

@schedule_bp.route('/today', methods=['POST'])

def set_todays_schedule():
    return []