from yad2_scraper import fetch_vehicle_category, Field
import pandas as pd
import json


from yad2_scraper import Yad2Scraper, Yad2Category, QueryFilters, OrderBy
from yad2_scraper.vehicles import (
    Yad2VehiclesCategory,
    VehiclesQueryFilters,
    OrderVehiclesBy,
    get_vehicle_category_url
)

scraper = Yad2Scraper(request_defaults={"timeout": 5}, max_request_attempts=3)

# Fetch businesses-for-sale category with filters
url = "https://www.yad2.co.il/vehicles/cars?manufacturer=40&model=10544%2C10541%2C10550&year=2021-2023&engineval=1200--1&hand=0-1&ownerID=1&yad2_source=HP_all_latestSearches"
# query_filters = QueryFilters(price_range=(10000, 250000), order_by=OrderBy.PRICE_LOWEST_TO_HIGHEST)
# businesses_for_sale_category = scraper.fetch_category(url, Yad2Category)#, params=query_filters)
# data = businesses_for_sale_category.load_next_data().get_data()

# Initialize the vehicle category scraper
cars_category = fetch_vehicle_category("cars")

# Load the first page of data
data = cars_category.load_next_data().get_data()

for car_data in cars_category.load_next_data().get_data():
    print(car_data.model(Field.ENGLISH_TEXT))
    print(car_data.test_date)
    print(car_data.price)

# # Extract relevant fields
# records = []
# for car in data:
#     record = {
#         "Model": car.model(Field.ENGLISH_TEXT),
#         "Year": car.year_of_production,
#         "Price": car.price,
#         "Hand": car.hand,
#         "Test Date": car.test_date,
#         "Engine Volume": car.engine_volume,
#         "Location": car.location,
#         "Link": car.page_link
#     }
#     records.append(record)
#
# # Create a DataFrame
# df = pd.DataFrame(records)
#
# # Export to Excel
# df.to_excel("yad2_cars.xlsx", index=False)
#
