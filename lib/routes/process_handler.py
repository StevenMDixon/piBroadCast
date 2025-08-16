import sys
import subprocess
import threading

auto_schedule_process = None
do_run_auto_schedule = False

def stop_auto_scheduler() -> None:
    global auto_schedule_process
    global do_run_auto_schedule

    do_run_auto_schedule = False
    if auto_schedule_process is not None:
        auto_schedule_process.terminate()
        auto_schedule_process = None

def run_scheduler(command) -> None:
    global auto_schedule_process
    if auto_schedule_process is None or auto_schedule_process.poll() is not None:
        auto_schedule_process = subprocess.Popen([sys.executable, "scheduler_sub.py", command])
    return

def run_auto_schedule() -> None:
    global auto_schedule_process
    global do_run_auto_schedule

    if not do_run_auto_schedule:
        do_run_auto_schedule = True
        runner()


def runner() -> None:
    global auto_schedule_process
    global do_run_auto_schedule

    if do_run_auto_schedule:
        if auto_schedule_process is None or auto_schedule_process.poll() is not None:
            auto_schedule_process = subprocess.Popen([sys.executable, "scheduler_sub.py", "--Schedule"])

        threading.Timer(60, runner).start() # Schedule run_auto_schedule after 1 minute