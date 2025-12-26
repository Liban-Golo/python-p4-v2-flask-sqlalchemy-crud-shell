# server/app.py

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake  # make sure your Earthquake model is in models.py

# create a Flask application instance 
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# -----------------------
# Routes
# -----------------------
@app.route('/')
def index():
    return '<h1>Welcome to the Flask-SQLAlchemy CRUD Shell Lab!</h1>'

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    quakes = Earthquake.query.all()
    return jsonify([q.to_dict() for q in quakes]), 200

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake:
        return jsonify(quake.to_dict()), 200
    return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200

# -----------------------
# Run the app
# -----------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
