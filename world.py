import json
import mysql.connector
from decimal import Decimal

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database="world"
)

cursor = db_connection.cursor()

query = "SELECT * FROM Country"
cursor.execute(query)

countries = []
for row in cursor.fetchall():
    country = {
        "Code": row[0],
        "Name": row[1],
        "Continent": row[2],
        "Region": row[3],
        "Surface area": row[4],
        "IndepYear": row[5],
        "Population": row[6],
        "LifeExpectancy": row[7],
        "GNP": row[8],
        "GNROld": row[9],
        "LocalName": row[10],
        "GovernmentForm": row[11],
        "HeadOfState": row[12],
        "Capital": row[13],
        "Code2": row[14],
        
        "Cities": [],
        "Languages": []
    }

    city_query = f"SELECT * FROM City WHERE CountryCode = '{country['Code']}'"
    cursor.execute(city_query)

    for city_row in cursor.fetchall():
        city = {
            "Name": city_row[1],
            "District": city_row[3],
            "Population": float(city_row[4])  
        }
        country["Cities"].append(city)

    language_query = f"SELECT * FROM CountryLanguage WHERE CountryCode = '{country['Code']}'"
    cursor.execute(language_query)

    for language_row in cursor.fetchall():
        language = {
            "Language": language_row[1],
            "IsOfficial": language_row[2],
            "Percentage": float(language_row[3])  
        }
        country["Languages"].append(language)

    countries.append(country)

cursor.close()
db_connection.close()

with open('countries_with_cities_and_languages.json', 'w', encoding='utf-8') as json_file:

    json.dump(countries, json_file, ensure_ascii=False, indent=4, default=str)

print("Данные успешно сохранены в countries_with_cities_and_languages.json")
