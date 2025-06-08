from yad2_scraper import fetch_vehicle_category, Field
import pandas as pd
import json

"""
/venv/lib/python3.13/site-packages/yad2_scraper/__init__.py
url = "https://www.yad2.co.il/vehicles/cars?manufacturer=40&model=10544%2C10541%2C10550&year=2021-2023&engineval=1200--1&hand=0-1&ownerID=1&yad2_source=HP_all_latestSearches"

"""

from yad2_scraper import Yad2Scraper, Yad2Category, QueryFilters, OrderBy
from yad2_scraper.vehicles import (
    Yad2VehiclesCategory,
    VehiclesQueryFilters,
    OrderVehiclesBy,
    get_vehicle_category_url
)

scraper = Yad2Scraper(request_defaults={"timeout": 5}, max_request_attempts=3)

# Fetch businesses-for-sale category with filters
# url = "https://www.yad2.co.il/vehicles/cars?manufacturer=40&model=10544%2C10541%2C10550&year=2021-2023&engineval=1200--1&hand=0-1&ownerID=1&yad2_source=HP_all_latestSearches"
# url_cars = "https://www.yad2.co.il/vehicles/cars"
# query_filters = QueryFilters(price_range=(10000, 120000), order_by=OrderBy.PRICE_LOWEST_TO_HIGHEST)
# businesses_for_sale_category = scraper.fetch_category(url_cars, Yad2Category, params=query_filters)
#
# for c in businesses_for_sale_category.load_next_data():
#     print(c)


# data = businesses_for_sale_category.load_next_data().get_data()

# Initialize the vehicle category scraper
_url = "https://www.yad2.co.il/vehicles/cars?manufacturer=37&model=10507&year=2023-2023&km=0-50000&hand=0-1&yad2_source=HP_all_latestSearches"
cars_category = fetch_vehicle_category("cars", url=_url)

# Load the first page of data
data = cars_category.load_next_data().get_data()

# count = 0
# for car_data in cars_category.load_next_data().get_data():
#     if car_data.manufacturer(Field.ENGLISH_TEXT) is not None:
#         count += 1
#         print(f"{car_data.model(Field.ENGLISH_TEXT)=}")
#         print(car_data.created_at)
#         print(car_data.updated_at)
#         print(car_data.rebounced_at)
#         print(car_data.year_of_production)
#         print(car_data.km)
#         print(car_data.price)
#         print(car_data.customer.get('agencyName'))
#         print(car_data.customer.get('name'))
#         print(car_data.customer_name)
#         print(car_data.customer.get('id'))




# print(f"Found {count} cars in total")


from openpyxl import Workbook

# Create a workbook and worksheet
wb = Workbook()
ws = wb.active
ws.title = "Vehicles"

EXPORT_FIELDS = ["created_at", "updated_at", "rebounced_at", "year_of_production", "km", "price"]


# Write headers
ws.append(EXPORT_FIELDS)

# Write filtered data from each VehicleData instance
for vehicle in cars_category.load_next_data().get_data():
    if vehicle.manufacturer(Field.ENGLISH_TEXT) is not None:
        row = [getattr(vehicle, field, "") for field in EXPORT_FIELDS]
    ws.append(row)

# Save the file
wb.save("vehicles_output.xlsx")
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
