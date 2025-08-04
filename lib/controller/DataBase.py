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
                schedule_date TEXT,
                schedule_file_name TEXT,         
                id INTEGER PRIMARY KEY
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episode_metadata (
                show_name TEXT,
                episode_name TEXT,
                episode_location TEXT,
                episode_length INTEGER,
                media_type TEXT,
                play_count INTEGER,
                bumper_data TEXT,
                id INTEGER PRIMARY KEY
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS station_config (
                station_name TEXT,
                subtitles INTEGER,
                playlist_location TEXT,
                playlist_file TEXT,
                start_time INTEGER,
                id INTEGER PRIMARY KEY
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule_template (
                template_data BLOB,
                id INTEGER PRIMARY KEY
            )
        ''')


        db.commit()

    def _get_conn():
        return sqlite3.connect('my_local_database.db')


