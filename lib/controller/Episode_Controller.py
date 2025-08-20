from lib.controller.DataBase import DataBase
from lib.models.dto import EpisodeData

class Episode_Controller:
    @staticmethod
    def _convert(data) -> EpisodeData:
        return EpisodeData(*data)
    
    @staticmethod
    def _convert_list(data) -> list[EpisodeData]:
        converted = []
        for i in data:
            converted.append(EpisodeData(*i))
        return converted

    @staticmethod
    def get_episode_metadata() -> EpisodeData:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM episode_metadata where id = {id}")
        episode_data = cursor.fetchone()
        return Episode_Controller.convert(episode_data)
     
    @staticmethod
    def get_all_episode_metadata() -> list[EpisodeData]:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM episode_metadata")
        records = cursor.fetchall()
        if records is None:
            return []
        else:
            return Episode_Controller._convert_list(records)
    
    @staticmethod
    def get_all_episode_metadata_by_type(type) -> list[EpisodeData]:
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM episode_metadata where media_type = ?", (type,))
        return Episode_Controller._convert_list(cursor.fetchall())
    
    @staticmethod
    def get_all_episode_metadata_by_type_by_lowest_play_count(type, show_name, already_played) -> list[EpisodeData]:
        db = DataBase._get_conn()
        cursor = db.cursor()

        if len(already_played) > 0:
            placeholders = ', '.join('?' * len(already_played))
            sql = f"SELECT * FROM episode_metadata where media_type = ? and show_name = ? and id not in ({placeholders}) ORDER BY play_count ASC LIMIT 20"
            params = (type, show_name, *already_played)
        else:
            sql = f"SELECT * FROM episode_metadata where media_type = ? and show_name = ? ORDER BY play_count ASC LIMIT 20"
            params = (type, show_name)

        cursor.execute(sql, params)
        return Episode_Controller._convert_list(cursor.fetchall())
    
    @staticmethod
    def get_all_commercials_by_tag(tag) -> list[EpisodeData]:
        db = DataBase._get_conn()
        cursor = db.cursor()
        type = 'commercial'

        where_clause = f"AND (tags like '%{tag}%' or tags = '')" if tag != "" else ""

        sql =  f"SELECT * FROM episode_metadata where media_type = '{type}' {where_clause} ORDER BY play_count ASC LIMIT 20"
      
        cursor.execute(sql)
        return Episode_Controller._convert_list(cursor.fetchall())
    
    @staticmethod
    def get_all_bumpers_by_tag(tag) -> list[EpisodeData]:
        db = DataBase._get_conn()
        cursor = db.cursor()
        type = 'bumper'

        where_clause = f"AND (tags like '%{tag}%' or tags = '')" if tag != "" else ""

        sql =  f"SELECT * FROM episode_metadata where media_type = '{type}' {where_clause} ORDER BY play_count ASC LIMIT 20"
      
        cursor.execute(sql)
        return Episode_Controller._convert_list(cursor.fetchall())


    @staticmethod
    def delete_all_episode_metadata() -> None: 
        db = DataBase._get_conn()
        cursor = db.cursor()
        cursor.execute("DELETE FROM episode_metadata")
        db.commit()
        db.close()

    @staticmethod
    def insert_episodes(episodes: list[EpisodeData]):
        db = DataBase._get_conn()
        cursor = db.cursor()
        prepared = [tuple(episode) for episode in episodes]
        cursor.executemany("insert into episode_metadata (show_name, episode_name, episode_location, episode_length, media_type, play_count, tags) values (?,?,?,?,?,?,?)", prepared)
        db.commit()
        db.close()

    @staticmethod
    def increment_played_count(episodes: list):
        db = DataBase._get_conn()
        cursor = db.cursor()

        prepared = [tuple([id]) for id in episodes]
        cursor.executemany("UPDATE episode_metadata SET play_count = play_count + 1 WHERE id = ? ", prepared)
        db.commit()
        db.close()
