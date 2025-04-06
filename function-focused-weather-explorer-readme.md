# Weather Explorer

Weather Explorer is a comprehensive weather application that allows you to check, save, and analyze weather data for any location worldwide.

## Core Functions Explained

### Location and Weather Functions

#### `get_coordinates(location)`
- **What it does:** Converts a location name (like "New York") into precise latitude and longitude coordinates
- **How it works:** Uses Google Maps Geocoding API to validate and locate places
- **When to use:** Any time you need to convert a place name into geographical coordinates
- **Example:** Enter "Paris" and get coordinates (48.8566, 2.3522)

#### `get_current_weather(location)`
- **What it does:** Retrieves the current temperature and weather description for any location
- **How it works:** Takes a location name, gets its coordinates, then fetches weather data from OpenWeather API
- **When to use:** When you want to know the current weather conditions anywhere in the world
- **Example:** Enter "Tokyo" to see it's 22°C and partly cloudy

#### `validate_date(date_str)`
- **What it does:** Checks if a date is formatted correctly (YYYY-MM-DD)
- **How it works:** Attempts to parse the date string to ensure it's valid
- **When to use:** When entering dates for weather requests to prevent errors
- **Example:** "2023-04-15" passes validation, "04/15/2023" fails

#### `get_weather_icon(description)`
- **What it does:** Converts weather descriptions into appropriate emoji icons
- **How it works:** Maps text descriptions like "clear sky" or "light rain" to corresponding weather emojis
- **When to use:** Used automatically to visualize weather conditions in the interface
- **Example:** "Rain" becomes 🌧️, "Clear" becomes ☀️

### Database Management Functions

#### `create_weather_request(location, start_date, end_date)`
- **What it does:** Saves weather information for a location and date range to the database
- **How it works:** Validates the input data, fetches current weather, and stores it all in the database
- **When to use:** When you want to track weather for a specific location over time
- **Example:** Save weather for "London" from April 1-7, 2023

#### `read_weather_requests()`
- **What it does:** Retrieves all saved weather records from the database
- **How it works:** Performs a database query to get all weather information you've stored
- **When to use:** When viewing your saved weather data or preparing for analysis
- **Example:** View all weather records you've saved for different locations

#### `update_weather_request(record_id, new_temp, new_desc)`
- **What it does:** Modifies the temperature or description of an existing weather record
- **How it works:** Updates specific fields in the database for a particular record ID
- **When to use:** When you need to correct or update weather information
- **Example:** Update record #5 to show 18°C instead of 15°C

#### `delete_weather_request(record_id)`
- **What it does:** Removes a weather record from the database
- **How it works:** Deletes the specified record completely from storage
- **When to use:** When you no longer need a particular weather record
- **Example:** Delete record #3 for "Miami" that you no longer need

### Media and Export Functions

#### `get_youtube_videos(location)`
- **What it does:** Finds YouTube videos about weather for a specific location
- **How it works:** Searches YouTube using its API for videos matching the location + "weather"
- **When to use:** When you want to see video forecasts or reports about a location
- **Example:** Search for "New York weather" videos

#### `export_to_csv(filename)`
- **What it does:** Exports all your weather data to a CSV file for use in other applications
- **How it works:** Converts the database records into a structured CSV format
- **When to use:** When you need to analyze your weather data in Excel or other tools
- **Example:** Export all your weather data to "weather_data.csv"

### User Interface Functions

#### Dashboard View
- **What it does:** Shows current weather and quick statistics
- **How it works:** Provides a search box for locations and displays weather with visual elements
- **When to use:** When you want to quickly check weather conditions
- **Features:** Temperature display, weather description, location statistics

#### Weather Requests View
- **What it does:** Manages your saved weather data
- **How it works:** Provides interfaces for creating, viewing, updating, and deleting weather records
- **When to use:** When you need to organize your weather information
- **Features:** Create requests with custom date ranges, search/filter saved requests

#### Weather Analysis View
- **What it does:** Visualizes your weather data in charts and graphs
- **How it works:** Processes your saved weather data into meaningful visualizations
- **When to use:** When you want to understand weather patterns and trends
- **Features:** Temperature distribution, location comparisons, monthly trends

#### Media & Export View
- **What it does:** Finds related media content and exports your data
- **How it works:** Searches for weather videos and prepares data exports in different formats
- **When to use:** When you need weather information in other formats or media
- **Features:** YouTube video search, CSV/JSON export with filtering options

## Using the Application

1. **Start the app** with `streamlit run app.py`
2. **Navigate** using the sidebar menu
3. **Search for locations** to get current weather
4. **Save weather data** for locations you're interested in
5. **Analyze trends** using the visualization tools
6. **Export data** when you need to use it elsewhere

Each function in Weather Explorer is designed to work together seamlessly, allowing you to move from checking current conditions to analyzing long-term trends with just a few clicks.
