import subprocess
import sys
import json
from flask import Blueprint, jsonify, request
from lib.controller.Schedule_Controller import Schedule_Controller
from lib.controller.Schedule_Template_Controller import Schedule_Template_Controller
from lib.models.dto import ScheduleTemplateData, ScheduleData
from datetime import datetime
from lib.routes.process_handler import run_auto_schedule, run_scheduler, stop_auto_scheduler

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')

process = None

@schedule_bp.route('/')

def get_schedule():
    return Schedule_Controller.get_schedules()

@schedule_bp.route('/template/file', methods=['POST'])

def set_schedule_template_from_file():
    data = request.json
    with open(data['template_file'], 'rb') as file:
    # Load the JSON data from the file into a Python dictionary or list
       myfile = file.read()
       Schedule_Template_Controller.set_schedule_template(myfile)

    return "",200

@schedule_bp.route('/template/data', methods=['POST'])

def set_schedule_template_from_data():
    data = json.dumps(request.json)
    Schedule_Template_Controller.set_schedule_template(data.encode('utf-8'))
    return "", 200

@schedule_bp.route('/template', methods=['GET'])

def get_schedule_template():
    data = Schedule_Template_Controller.get_current_schedule_template()
    print(data)
    decoded = json.loads(data.template_data.decode('utf-8'))
    return jsonify(decoded), 200

@schedule_bp.route('/today', methods=['GET'])

def get_todays_schedule():
    response = Schedule_Controller.get_todays_schedule(datetime.today().date())
    if response is not None:
        return jsonify(response), 200
    return "No Schedule Found", 204

@schedule_bp.route('/run/rebuild', methods=['GET'])

def run_rebuild_schedule():
    run_scheduler("--Rebuild")
    return "Rebuilding schedule database", 200

@schedule_bp.route('/run/build', methods=['GET'])

def run_build_schedule():
    run_scheduler("--Build")
    return "Building schedule database", 200

@schedule_bp.route('/run/schedule', methods=['GET'])

def run_create_schedule():
    run_scheduler("--Schedule")
    return "Creating schedules", 200

@schedule_bp.route('/run/auto', methods=['POST'])
def run_auto():
    run_auto_schedule()
    return "", 204

@schedule_bp.route('/run/auto_stop', methods=['POST'])
def run_auto_stop():
    stop_auto_scheduler()
    return "Stopping automatic scheduling", 200

@schedule_bp.route('/delete', methods=['POST'])
def run_delete_schedule():
    Schedule_Controller.delete_all_schedules()
    return "", 204