from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return "<h1>Project Server</h1>"


@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        return make_response(jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200)

    return make_response(jsonify({
        "message": f"Earthquake {id} not found."
    }), 404)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    return make_response(jsonify({
        "count": len(quakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
            for quake in quakes
        ]
    }), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True) 