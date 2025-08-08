from flask import Blueprint, jsonify
from crontab import CronTab
import os

utility_bp = Blueprint('utility', __name__, url_prefix='/utils')

@utility_bp.route('/set_server_cron', methods=['POST'])

def set_server_cron():
    cron = CronTab(user=True)

    # Path to your script
    current_dir = os.getcwd()
    script_path = f'{current_dir}/scripts/start.sh'

    # Create a new job
    job = cron.new(command=f'{script_path}', comment='Run script at boot')

    # Set it to run at reboot
    job.every_reboot()

    # Write the job to the crontab
    cron.write()

    return jsonify({"message": "Cron job set"}), 200

@utility_bp.route('/set_schedule_cron', methods=['POST'])

def set_schedule_cron():
    cron = CronTab(user=True)

    # Path to your script
    current_dir = os.getcwd()
    venv_path = f'{current_dir}/venv/bin/python'
    script_path = f'{current_dir}/scheduler_sub.py "--Schedule"'

    # Create a new job
    job = cron.new(command=f'{venv_path} {script_path}', comment='Run script every hour')

    # Set it to run every hour
    job.hour.every(1)

    # Write the job to the crontab
    cron.write()

    return jsonify({"message": "Cron job set"}), 200

@utility_bp.route('/clear_cron', methods=['POST'])

def clear_cron():   
    cron = CronTab(user=True)
    cron.remove_all(comment='Run script every hour')
    cron.remove_all(comment='Run script at boot')
    cron.write()
    return jsonify({"message": "All cron jobs cleared"}), 200