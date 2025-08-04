import os
import sys
from lib.scheduler_lib.Scheduler import Scheduler

os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    #ingest the template and create a schedule.
    if len(sys.argv) > 1:
        Scheduler(sys.argv[1])
    else:
        Scheduler()
