from flask import Flask
import os
from routes.schedule_routes import schedule_bp
from routes.player_routes import player_bp
from routes.station_routes import station_bp

app = Flask(__name__)

app.register_blueprint(schedule_bp)
app.register_blueprint(player_bp)
app.register_blueprint(station_bp)

os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    
    app.run()