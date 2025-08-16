import sqlite3
from lib.controller.DataBase import DataBase
from lib.models.dto import StationConfig

class Station_Controller:
    @staticmethod
    def _convert(data: tuple) -> StationConfig:
        return StationConfig(*data)
    
    @staticmethod
    def _convert_list(data: list[tuple]) -> list[StationConfig]:
        converted = []
        for i in data:
            converted.append(StationConfig(*i))
        return converted
    
    @staticmethod
    def get_current_station_config() -> StationConfig | None:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM station_config ORDER BY id desc LIMIT 1")
        config = cursor.fetchone()

        if config is not None:
                return Station_Controller._convert(config)
        return None

    @staticmethod
    def add_station_config(station_config) -> None:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("INSERT INTO station_config (station_name, playlist_location, playlist_file, start_time) VALUES (?,?,?,?)", tuple(station_config))
        db.commit()
        db.close()