from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": "*"}}) #TODO: make UI URL variable for production server
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
migration HOW-TO:
docker-compose run backend flask db init
docker-compose run backend flask db migrate -m "Initial migration."
docker-compose run backend flask db upgrade
flask db downgrade
'''

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="culturedb",
        user="postgres",
        password="postgres"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT 1')
    cur.close()
    conn.close()
    return 'Hello, CultureDB!'

@app.route('/api/search', methods=['POST'])
def search():
    # Extracting the search parameters from the request
    data = request.get_json()
    where = data.get('where', '')
    when = data.get('when', '')
    priceRange = data.get('priceRange', '')
    type = data.get('type', '')
    author = data.get('author', '')
    title = data.get('title', '')

    # For demonstration, returning a list of three elements with default values
    results = [
        {
            'location': 'New York',
            'datetime': '2024-07-10T19:30:00',
            'webpage': 'https://example.com/event1',
            'title': 'Event 1',
            'price': '$20'
        },
        {
            'location': 'London',
            'datetime': '2024-07-11T20:00:00',
            'webpage': 'https://example.com/event2',
            'title': 'Event 2',
            'price': '£15'
        },
        {
            'location': 'Berlin',
            'datetime': '2024-07-12T18:00:00',
            'webpage': 'https://example.com/event3',
            'title': 'Event 3',
            'price': '€10'
        }
    ]

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)