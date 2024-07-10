from flask import Flask
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)