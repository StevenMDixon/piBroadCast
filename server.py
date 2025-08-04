from flask import Flask
from lib.controller.DataBase import DataBase
import os
from lib.routes.schedule_routes import schedule_bp
from lib.routes.player_routes import player_bp
from lib.routes.station_routes import station_bp
from lib.routes.episode_routes import episode_bp
from flasgger import Swagger

app = Flask(__name__)

app.register_blueprint(schedule_bp)
app.register_blueprint(player_bp)
app.register_blueprint(station_bp)
app.register_blueprint(episode_bp)

os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    DataBase()

    Swagger(app)
    app.run()