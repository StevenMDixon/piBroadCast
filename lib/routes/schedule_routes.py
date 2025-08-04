import json
from flask import Blueprint, jsonify, request
from lib.controller.Schedule_Controller import Schedule_Controller
from lib.controller.Schedule_Template_Controller import Schedule_Template_Controller
from lib.models.dto import ScheduleTemplateData, ScheduleData

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@schedule_bp.route('/')

def get_schedule():
    return Schedule_Controller.get_schedules()

@schedule_bp.route('/template', methods=['POST'])

def set_schedule_template():
    data = request.json
    with open(data['template_file'], 'rb') as file:
    # Load the JSON data from the file into a Python dictionary or list
       myfile = file.read()
       Schedule_Template_Controller.set_schedule_template(myfile)

    return "",200

@schedule_bp.route('/today', methods=['GET'])

def get_todays_schedule():
    response = Schedule_Controller.get_todays_schedule('7/31/25')
    if response is not None:
        return jsonify(ScheduleData(**response)), 200
    return "", 204

@schedule_bp.route('/today', methods=['POST'])

def set_todays_schedule():
    data = request.json
    schedule = ScheduleData(**data)
    Schedule_Controller.set_todays_schedule(schedule)
    return 'success', 202