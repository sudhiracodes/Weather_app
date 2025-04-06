

## Overview

Weather Explorer is a comprehensive weather data management and analysis platform built with Streamlit. The application allows users to fetch current weather information for any location worldwide, store historical weather data, analyze weather trends, and export data for further analysis.

## Features

### 1. Dashboard
- **Current Weather Display**: Get real-time weather information for any location with visual representation
- **Quick Stats**: View aggregated statistics like total requests, most searched locations, and average temperatures
- **Recent Locations**: Track your latest searched locations

### 2. Weather Requests Management
- **Create Requests**: Save weather data for specific locations and date ranges
- **View Requests**: Browse all saved weather requests with search and filter options
- **Update Requests**: Modify temperature and weather descriptions for existing records
- **Delete Requests**: Remove unwanted weather data records

### 3. Weather Analysis & Trends
- **Temperature Distribution**: Visualize temperature distribution with statistical metrics
- **Location Analysis**: Compare temperatures across different locations
- **Time Trends**: Track temperature changes over time with monthly breakdowns

### 4. Media & Export
- **YouTube Videos**: Find weather-related videos for specific locations
- **Export Data**: Export weather data in CSV or JSON format with customizable filters

## Installation

### Prerequisites
- Python 3.6+
- SQLite3
- Required Python packages (see requirements.txt)

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-explorer.git
   cd weather-explorer
   ```

2. Install dependencies:
   ```
   pip install requests streamlit
   ```

3. Set up your API keys:
   - OpenWeather API: Get from [OpenWeather](https://openweathermap.org/api)
   - Google Maps API: Get from [Google Cloud Platform](https://console.cloud.google.com/)
   - YouTube API: Get from [Google Cloud Platform](https://console.cloud.google.com/)

   Replace the placeholder API keys in the app.py file:
   ```python
   OPENWEATHER_API_KEY = "your_openweather_api_key"
   GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
   YOUTUBE_API_KEY = "your_youtube_api_key"
   ```

## Usage

### Starting the Application
Run the application with:
```
streamlit run app.py
```

The application will be available at [http://localhost:8501](http://localhost:8501)

### Core Functionality

#### Getting Current Weather
1. Navigate to the Dashboard
2. Enter a location (city name, ZIP code, or coordinates)
3. Click "Get Weather" to view current weather information

#### Creating Weather Requests
1. Go to Weather Requests > Create Request
2. Enter a location and select a time range
3. Add optional notes
4. Click "Save Request"

#### Analyzing Weather Data
1. Go to Weather Analysis tab
2. Explore different visualizations across the three tabs:
   - Temperature Distribution
   - Location Analysis
   - Time Trends

#### Exporting Data
1. Go to Media & Export > Export Data
2. Select export format (CSV or JSON)
3. Set date range and location filters
4. Click "Export Data"

## Function Reference

### Location and Weather Functions
- `get_coordinates(location)`: Validates location and retrieves geographical coordinates
- `get_current_weather(location)`: Fetches current weather for a specified location
- `get_weather_icon(description)`: Maps weather descriptions to emoji icons

### Database Operations
- `create_weather_request(location, start_date, end_date)`: Stores weather request in the database
- `read_weather_requests()`: Retrieves all weather requests
- `update_weather_request(record_id, new_temp, new_desc)`: Updates an existing weather record
- `delete_weather_request(record_id)`: Removes a weather record from the database

### Utility Functions
- `validate_date(date_str)`: Validates date format
- `get_youtube_videos(location)`: Fetches YouTube videos related to weather for a location
- `export_to_csv(filename)`: Exports weather data to CSV format

### UI Components
- `main()`: Main application entry point that handles UI rendering and navigation

## Database Schema

The application uses SQLite3 with a single table structure:

```sql
CREATE TABLE weather_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    start_date TEXT,
    end_date TEXT,
    temperature REAL,
    weather_desc TEXT,
    request_time TEXT
)
```

## Customization

### Styling
The application includes custom CSS for better styling. You can modify the styles in the `st.markdown()` section of the `main()` function.


## Acknowledgements

- Weather data provided by [OpenWeather API](https://openweathermap.org/api)
- Geocoding by [Google Maps API](https://developers.google.com/maps/documentation/geocoding/overview)
- Video content from [YouTube Data API](https://developers.google.com/youtube/v3)
