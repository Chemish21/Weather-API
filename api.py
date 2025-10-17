#Python
#Necessary modules
from fastapi import FastAPI
from datetime import date
from dotenv import load_dotenv
import os
import sys
import re
import requests
import json
import redis

#Loading environment data
load_dotenv()

#Setting user key from environment
api_key = os.getenv("API_KEY")

#Setting FastAPI and Redis variables
app = FastAPI()
red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

#Function to gather todays weather data and send to JSON file/Redis cache
def get_today(location: str):
  request = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/?key={api_key}")
  with open("weather.json", "w") as json_file:
    #Get data and store "days" list
    weather_info = request.json()
    the_days = weather_info["days"]

    #Gather necessary data and stop after first day
    for days in the_days:
        date = days["datetime"]
        high = days["tempmax"]
        low = days["tempmin"]
        rain_chance = days["precipprob"]
        snow_chance = days["snow"]
        conditions = days["conditions"]
        if days["hours"]:
          break   
    #Send data to Redis cache and JSON file
    red.set("today", json.dumps([date, conditions, high, low, rain_chance, snow_chance]), ex=43200)
    json.dump(weather_info, json_file, indent=2)

#Function to find total days between input start/end dates
def get_total_days(start_date, end_date):
  #Seperate YYYY-MM-DD by group
  start_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", start_date)
  end_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", end_date)

  #Store dates as integers for comparison
  if start_match:
    st_year, st_month, st_day = map(int, start_match.groups())
  if end_match:
    end_year, end_month, end_day = map(int, end_match.groups())

  #Setting dates
  date1 = date(st_year, st_month, st_day)
  date2 = date(end_year, end_month, end_day)

  #Find total days between dates and return total
  difference = date2 - date1
  total_days = difference.days
  return total_days

#Function to gather weather data between start/end dates and send to JSON file/Redis cache
def get_range(location: str):
  #List to hold day to day weather information
  range_days = []

  #Informing user and getting start/end dates
  print("Format: YYYY-MM-DD Limit: 31 days")
  print("---------------------------------")
  start_date = input("Enter starting date: ")
  end_date = input("Enter ending date: ")
  print()

  #Setting total days betwen start/end dates
  total_days = get_total_days(start_date, end_date)

  #Total days not to exceed limit
  if total_days > 31:
    print("Limit: 31 days")
    sys.exit()
  else:
    request = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?key={api_key}")
    with open("weather.json", "w") as json_file:
      #Get data and store "days" list
      weather_info = request.json()
      the_days = weather_info["days"]

      #Gather necessary data and append to list after each day
      for days in the_days:
          date = days["datetime"]
          high = days["tempmax"]
          low = days["tempmin"]
          rain_chance = days["precipprob"]
          snow_chance = days["snow"]  
          conditions = days["conditions"]
          if days["hours"]:
            day = [date, conditions, high, low, rain_chance, snow_chance]
            range_days.append(day)
      #Send data to Redis cache and JSON file
      red.set("range", json.dumps(range_days), ex=43200)
      json.dump(weather_info, json_file, indent=2)

#If we recieve a GET request, display today data from Redis
@app.get("/weather/today")
async def display_today():
  weather = red.get("today")
  if not weather:
    return {"today": "Information unavailable at this time"}
  date, conditions, high, low, rain_chance, snow_chance = json.loads(weather)
  return {"today": f"{date}: {conditions}, High:{high}, Low:{low}, Rain:{rain_chance}%, Snow:{snow_chance}%"}

#If we recieve a GET request, display range data from Redis
@app.get("/weather/range")
async def display_range():
  weather = red.get("range")
  if not weather:
    return {"range": "Information unavailable at this time"}
  return {"range": f"{weather}"}
