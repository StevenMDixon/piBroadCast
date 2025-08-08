import sqlite3
from lib.controller.DataBase import DataBase
from lib.models.dto import ScheduleTemplateData

class Schedule_Template_Controller:
    @staticmethod
    def _convert(data: tuple) -> ScheduleTemplateData:
        return ScheduleTemplateData(*data)
    
    @staticmethod
    def _convert_list(data: list[tuple]) -> list[ScheduleTemplateData]:
        converted = []
        for i in data:
            converted.append(ScheduleTemplateData(*i))
        return converted

    @staticmethod
    def get_current_schedule_template() ->ScheduleTemplateData:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_template ORDER BY id desc LIMIT 1")
        config = cursor.fetchone()

        if config is not None:
            return Schedule_Template_Controller._convert(config)
        return None
    
    @staticmethod
    def set_schedule_template(template_file_data):
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("INSERT INTO schedule_template (template_data) VALUES (?)", (sqlite3.Binary(template_file_data),))
        db.commit()
        db.close()
