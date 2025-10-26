# Weather-API
A Command Line Interface program that displays weather data gathered from VisualCrossing API  
Data is stored via Redis caching and a JSON file  
Idea taken from suggested projects by roadmap.sh  
Source: https://roadmap.sh/projects/weather-api-wrapper-service  

**Usage**: python3 weath.py [command]
User must provide their own API key and store in a .env file  
Key can be obtained after creating an account with VisualCrossing  
Site: https://www.visualcrossing.com/  

**Commands**:  
**-t or --today** gets and displays todays weather information  
**-r or --range** gets and displays weather data between a start/end date. Limit set to 31 days currently.
