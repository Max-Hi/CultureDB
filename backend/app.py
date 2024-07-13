from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
# for geological distances
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
# for typing: 
from typing import Any, List, Dict, Tuple
# for webcrawling:
import requests
from bs4 import BeautifulSoup
# for logging
import logging

load_dotenv()  # Load environment variables from .env file


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)#, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": "*"}}) #TODO: make UI URL variable for production server
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

# temporary? TODO into databank? List of cultural places
culture_spaces = {
        "frankfurter_schauspiel": {
            "name": "Schauspielhaus Frankfurt",
            "type": "Theater",
            "city": "Frankfurt",
            "price_range": [15,50], #TODO include or get via webcrawler?
            "webpage": "https://www.schauspielfrankfurt.de",
            "...": "todo"
        },    
        "frankfurter_oper": {
            "name": "Oper Frankfurt",
            "type": "Oper",
            "city": "Frankfurt",
            "...": "todo"
        },
        "heidelberger_theater": {
            "name": "Theater und Orchester Heidelberg",
            "type": "Theater",
            "city": "Heidelberg",
            "...": "todo"
        },
        "karlstorkino_heidelberg": {
            "name": "Karlstorkino",
            "type": "Kino",
            "city": "Heidelberg",
            "webpage": "https://www.karlstorkino.de/index.php?RUBRIK=5&Document=13",
            "config": {
                "...": "todo",
            }
        },
        "schauburg": {
            "name": "Schauburg",
            "type": "Kino",
            "city": "Karlsruhe",
            "...": "todo"
        },
            
    }






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


################ for filtering by location #################
def get_coordinates(city_name: str) -> Tuple[float, float]:
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        raise ValueError("City not found")

def filter_by_proximity(city: str, max_distance: int) -> List[Any]: #TODO: better return type hint
    city_coords = get_coordinates(city)
    filtered_elements = {}
    for place, info in culture_spaces.items():
        element_coords = get_coordinates(info['city'])
        distance = geodesic(city_coords, element_coords).kilometers
        if distance < max_distance:
            filtered_elements[place] = info
    return filtered_elements



################ webcrawler #################
def get_html_content(url: str) -> bytes:
    '''returns the html code of the given URL'''
    response = requests.get(url)
    return response.content

def parse_events(html_content: bytes, config: Dict[str, Any]) -> List[Any]: #TODO better type hint for return
    '''takes the html content from a website and config on how to derive events from that website and creates a list with all events found in that html code'''
    #TODO: use config to make this work for general websites not just for Karlstorkino
    soup = BeautifulSoup(html_content, 'html.parser')
    events = []
    # Modify this part based on the website's structure
    app.logger.info("finding all a types of class LinkBold")
    for event in soup.find_all('a', class_='LinkBold'):
        app.logger.info(event.get("href"))
        app.logger.info(get_html_content("https://karlstorkino.de"+event.get("href")))
        # event_name = event.find('h3').text.strip()
        # event_date = event.find('span', class_='date').text.strip()
    #TODO events.append({....})
    return events # TODO dummy

def find_events(event_place_list: Dict[str,Dict[str, Any]]) -> List[Dict[str, Any]]:
    '''finds all events for implemented places that adhere to the given criteria'''
    # TODO criteria -> filter
    results = []
    for place, info in event_place_list.items():
        #TODO: call specialized crawler
        if place == "karlstorkino_heidelberg":
            parse_events(get_html_content(info["webpage"]), info["config"])
        # dummy implementation: 
        '''if place == "schauburg":
            results.append({'location': 'Karlsruhe',
            'datetime': '2024-07-10T19:30:00',
            'webpage': 'schauburg.de',
            'title': 'Kinds of Kindness',
            'price': '€10'})
        if place == "karlstorkino_heidelberg":
            results.append({'location': 'Heidelberg',
            'datetime': '2024-07-10T19:30:00',
            'webpage': 'karlstorkino.de',
            'title': 'Kinds of Kindness',
            'price': '€5'})
        if place == "frankfurter_oper":
            results.append({'location': 'Frankfurt',
            'datetime': '2024-07-10T19:30:00',
            'webpage': 'oper-frankfurt.de',
            'title': 'Tristan und Isolde',
            'price': '€100'})'''
    return results
    


################ API Calls go here #################
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

    app.logger.info("TESTTTTT")
    parse_events(get_html_content("https://www.karlstorkino.de/index.php?RUBRIK=5&Document=13"), dict())
    # For demonstration, returning a list of three elements with default values
    results = []#find_events(culture_spaces)#filter_by_proximity(where, int(when)))

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)