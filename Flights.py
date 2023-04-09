import requests
from bs4 import BeautifulSoup

class Flight:
    def __init__(self, origin, destination, start_date, end_date):
        self.origin, self.destination, self.start_date, self.end_date = origin, destination, start_date, end_date
        self.prices, self.flight_times, self.airlines = [], [], []
    
    def scrape(self):
        url = f"https://www.expedia.com/Flights-Search?flight-type=on&starDate={self.start_date}&endDate={self.end_date}&mode=search&trip=roundtrip&leg1=from%3A{self.origin}%2Cto%3A{self.destination}%2Cdeparture%3A{self.start_date}TANYT&leg2=from%3A{self.destination}%2Cto%3A{self.origin}%2Cdeparture%3A{self.end_date}TANYT&adults=2&children=0&infants=0&sort=price&ascending=true&inttkn=0d3v7xu8pvl0f&trav"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.prices = [float(price.text.strip().replace('$', '').replace(',', '')) for price in soup.find_all('span', {'data-test-id': 'listing-price-dollars'})]
        self.flight_times = [time.text.strip() for time in soup.find_all('span', {'data-test-id': 'duration'})]
        self.airlines = [airline.text.strip() for airline in soup.find_all('span', {'data-test-id': 'airline-name'})]

class Hotel:
    def __init__(self, location, start_date, end_date):
        self.location, self.start_date, self.end_date = location, start_date, end_date
        self.ratings, self.prices = [], []
    
    def scrape(self):
        pass

class Holiday:
    def __init__(self, budget, origin, destination, start_date, end_date):
        self.budget, self.flight, self.hotel = budget, Flight(origin, destination, start_date, end_date), Hotel(destination, start_date, end_date)
        self.recommendations = []
    
    def plan(self):
        self.flight.scrape()
        self.hotel.scrape()
        self.recommendations = self.flight.recommendations + self.hotel.recommendations
        self.recommendations = sorted(self.recommendations, key=lambda x: x['rating'] or x['price'])
        self.recommendations = [r for r in self.recommendations if r['price'] <= self.budget]
