import sqlite3
from lib.controller.DataBase import DataBase
from datetime import datetime
from lib.models.dto import ScheduleData


class Schedule_Controller:
    @staticmethod
    def _convert(data: tuple) -> ScheduleData:
        return ScheduleData(*data)
    
    @staticmethod
    def _convert_list(data: list[tuple]) -> list[ScheduleData]:
        converted = []
        for i in data:
            converted.append(ScheduleData(*i))
        return converted

    @staticmethod
    def get_schedules() -> list[ScheduleData]:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schedule_metadata")
        return Schedule_Controller._convert_list(cursor.fetchall())

    @staticmethod
    def get_schedule(id: int) -> ScheduleData:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata where id = ?", (id,))
        schedule_data = cursor.fetchone()
        return Schedule_Controller._convert(schedule_data)

    @staticmethod
    def get_todays_schedule(date: datetime) -> ScheduleData:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata where schedule_date = ?", (date, ))
        schedule_data = cursor.fetchone()
        if schedule_data is not None:
             return Schedule_Controller._convert(schedule_data)
        return None

    @staticmethod
    def get_lastest_schedule() -> ScheduleData:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata ORDER BY id desc LIMIT 1")
        latest_schedule = cursor.fetchone()
        if latest_schedule is not None:
            return  Schedule_Controller._convert(latest_schedule)
        return None

    @staticmethod
    def set_todays_schedule(schedule_data) -> None:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schedule_metadata (schedule_date, schedule_file_name) VALUES (?, ?)", (schedule_data['schedule_date'], schedule_data['schedule_file_name']))
        db.commit()
        db.close()


    @staticmethod
    def add_schedule(schedule_data) -> None:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schedule_metadata (schedule_date, schedule_file_name) VALUES (?, ?)", (schedule_data['schedule_date'], schedule_data['schedule_file_name']))
        db.commit()
        db.close()

    @staticmethod
    def add_scheduler_to_chron(id: int) -> None:
        pass