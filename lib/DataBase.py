import sqlite3

class DataBase():
    def __init__(self):
        self.init()

    def init(self):
        db = sqlite3.connect('my_local_database.db')
        # build our tables
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule_metadata (
                id INTEGER PRIMARY KEY,
                schedule_date TEXT,
                schedule_data BLOB         
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episode_metadata (
                id INTEGER PRIMARY KEY,
                show_name TEXT,
                last_played_season INTEGER,            
                last_played_episode INTEGER             
            )
        ''')
        
        db.commit()

    def _get_conn():
        return sqlite3.connect('my_local_database.db')

    @staticmethod
    def get_schedules():
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM schedule_metadata")
        return cursor.fetchall()
    
    @staticmethod
    def get_schedule( id):
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata where id = ?", id)
        return cursor.fetchone()[0]
    
    @staticmethod
    def get_todays_schedule(date):
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata where schedule_date = ?", date)
        return cursor.fetchone()[0]
    
    @staticmethod
    def set_todays_schedules(_):
        pass
    
    @staticmethod
    def get_episode_metadata():
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM schedule_metadata where id = {id}")
        return cursor.fetchone()[0]