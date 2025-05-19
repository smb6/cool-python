pip install yad2-scraper pandas openpyxl

venv/lib/python3.9/site-packages/yad2_scraper/vehicles/urls.py

VEHICLES_URL = "https://www.yad2.co.il/vehicles/cars?manufacturer=40&model=10544%2C10541%2C10550&year=2021-2023&engineval=1200--1&hand=0-1&ownerID=1&yad2_source=HP_all_latestSearches"


venv/lib/python3.9/site-packages/yad2_scraper/vehicles/next_data.py


    def jsonify(self):
        def default_serializer(obj):
            return str(obj)  # Fallback for non-serializable values like datetime

        return json.loads(json.dumps(self.data, default=default_serializer))