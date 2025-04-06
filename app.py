import streamlit as st
import sqlite3
import requests
from datetime import datetime, timedelta
import csv
import sys
import pandas as pd

# API Keys (replace with your own)
OPENWEATHER_API_KEY = ""
GOOGLE_MAPS_API_KEY = ""
YOUTUBE_API_KEY = ""

# Database setup
conn = sqlite3.connect("weather_app.db")
cursor = conn.cursor()

# Create table for weather data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_requests (
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
''')
conn.commit()

# Original functions (unchanged)
def get_coordinates(location):
    """Validate location and get coordinates using Google Maps Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "OK":
        lat = response["results"][0]["geometry"]["location"]["lat"]
        lng = response["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        raise ValueError("Invalid location or unable to geocode.")

def get_current_weather(location):
    """Fetch current weather for a given location."""
    try:
        lat, lng = get_coordinates(location)
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            print(f"Current Weather in {location}: {temp}°C, {desc}")
            return temp, desc, lat, lng
        else:
            print("Error fetching weather data.")
            return None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def create_weather_request(location, start_date, end_date):
    """Store weather request in the database."""
    if not validate_date(start_date) or not validate_date(end_date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return False
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if start > end:
        print("Start date must be before end date.")
        return False
    
    temp, desc, lat, lng = get_current_weather(location)
    if temp is not None:
        cursor.execute('''
            INSERT INTO weather_requests (location, latitude, longitude, start_date, end_date, temperature, weather_desc, request_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (location, lat, lng, start_date, end_date, temp, desc, datetime.now().isoformat()))
        conn.commit()
        print("Weather data saved successfully.")
        return True
    return False

def read_weather_requests():
    """Read all weather requests from the database."""
    cursor.execute("SELECT * FROM weather_requests")
    rows = cursor.fetchall()
    return rows

def update_weather_request(record_id, new_temp=None, new_desc=None):
    """Update a weather request."""
    cursor.execute("SELECT * FROM weather_requests WHERE id = ?", (record_id,))
    if not cursor.fetchone():
        print("Record not found.")
        return False
    
    if new_temp is not None and not isinstance(new_temp, (int, float)):
        print("Temperature must be a number.")
        return False
    
    if new_temp is not None:
        cursor.execute("UPDATE weather_requests SET temperature = ? WHERE id = ?", (new_temp, record_id))
    if new_desc is not None:
        cursor.execute("UPDATE weather_requests SET weather_desc = ? WHERE id = ?", (new_desc, record_id))
    
    conn.commit()
    print("Record updated successfully.")
    return True

def delete_weather_request(record_id):
    """Delete a weather request."""
    cursor.execute("SELECT * FROM weather_requests WHERE id = ?", (int(record_id),))
    if not cursor.fetchone():
        print("Record not found.")
        return False
    
    cursor.execute("DELETE FROM weather_requests WHERE id = ?", (int(record_id),))
    conn.commit()
    print("Record deleted successfully.")
    return True

def get_youtube_videos(location):
    """Fetch YouTube videos for a location."""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={location}+weather&type=video&key={YOUTUBE_API_KEY}&maxResults=3"
    response = requests.get(url).json()
    
    if "items" in response:
        videos = []
        for item in response["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            videos.append({"title": title, "url": f"https://www.youtube.com/watch?v={video_id}"})
        return videos
    return []

def export_to_csv(filename="weather_data.csv"):
    """Export weather data to CSV."""
    cursor.execute("SELECT * FROM weather_requests")
    rows = cursor.fetchall()
    
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Location", "Latitude", "Longitude", "Start Date", "End Date", "Temperature", "Description", "Request Time"])
        writer.writerows(rows)
    return filename

# Weather icon mapping
def get_weather_icon(description):
    description = description.lower()
    if "clear" in description:
        return "☀️"
    elif "sun" in description:
        return "🌞"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "thunder" in description:
        return "⛈️"
    elif "snow" in description:
        return "❄️"
    elif "mist" in description or "fog" in description:
        return "🌫️"
    else:
        return "🌦️"

# Streamlit UI
def main():
    # App configuration
    st.set_page_config(
        page_title="Weather Explorer",
        page_icon="🌦️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.8rem !important;
        font-weight: 600;
        color: #4682B4;
        border-bottom: 2px solid #4682B4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .weather-display {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 1.5rem;
        background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
        padding: 20px;
        border-radius: 15px;
        color: #333;
        text-align: center;
    }
    .weather-icon {
        font-size: 4rem;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .delete-button button {
        background-color: #f44336;
    }
    .delete-button button:hover {
        background-color: #d32f2f;
    }
    .update-button button {
        background-color: #2196F3;
    }
    .update-button button:hover {
        background-color: #0b7dda;
    }
    .youtube-card {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # App header
    st.markdown('<h1 class="main-header">🌦️ Weather Explorer</h1>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 30px;">
        Your comprehensive weather data management and analysis platform
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Sidebar styling and navigation
    with st.sidebar:
        st.image("https://i.imgur.com/8nLFCVP.png", width=100)  # You'll need to replace with a placeholder
        st.title("Navigation")
        
        # Create tabs-like effect with radio buttons
        menu = ["Dashboard", "Weather Requests", "Weather Analysis", "Media & Export"]
        main_choice = st.radio("", menu)
        
        # Conditional submenu based on main choice
        if main_choice == "Weather Requests":
            submenu = st.radio(
                "Request Options:", 
                ["Create Request", "View Requests", "Update Request", "Delete Request"]
            )
        elif main_choice == "Media & Export":
            submenu = st.radio(
                "Options:", 
                ["YouTube Videos", "Export Data"]
            )
        
        st.divider()
        st.markdown("### About")
        st.info("Weather Explorer helps you track and analyze weather patterns for any location worldwide.")
        
        # Show current time
        st.write(f"📅 {datetime.now().strftime('%B %d, %Y %H:%M')}")

    # Main content area
    if main_choice == "Dashboard":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<h2 class="subheader">Current Weather</h2>', unsafe_allow_html=True)
            
            # Location input with autocomplete feel
            location = st.text_input(
                "Enter Location:",
                placeholder="City name, ZIP code, or coordinates"
            )
            
            col_btn, col_empty = st.columns([1, 3])
            with col_btn:
                get_weather = st.button("Get Weather", use_container_width=True)
            
            if location and get_weather:
                with st.spinner("Fetching weather data..."):
                    temp, desc, lat, lng = get_current_weather(location)
                    
                    if temp is not None:
                        weather_icon = get_weather_icon(desc)
                        
                        st.markdown(
                            f"""
                            <div class="weather-display">
                                <div class="weather-icon">{weather_icon}</div>
                                <div style="font-size: 2.5rem; font-weight: bold;">{temp}°C</div>
                                <div style="text-transform: capitalize;">{desc}</div>
                                <div style="font-size: 1.2rem; margin-top: 10px;">{location}</div>
                                <div style="font-size: 0.9rem; opacity: 0.7;">Lat: {lat:.4f}, Long: {lng:.4f}</div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("Couldn't fetch weather data. Please check the location or API keys.")
        
        with col2:
            st.markdown('<h2 class="subheader">Quick Stats</h2>', unsafe_allow_html=True)
            
            # Get stats from database
            cursor.execute("SELECT COUNT(*) FROM weather_requests")
            total_requests = cursor.fetchone()[0]
            
            cursor.execute("SELECT location, COUNT(*) FROM weather_requests GROUP BY location ORDER BY COUNT(*) DESC LIMIT 1")
            top_location_result = cursor.fetchone()
            top_location = top_location_result[0] if top_location_result else "None"
            
            cursor.execute("SELECT AVG(temperature) FROM weather_requests")
            avg_temp = cursor.fetchone()[0]
            
            # Display metrics
            st.metric("Total Weather Requests", total_requests)
            st.metric("Most Searched Location", top_location)
            if avg_temp:
                st.metric("Average Temperature", f"{avg_temp:.1f}°C")
            
            # Show recent locations with minimize/expand
            with st.expander("Recent Locations"):
                cursor.execute("SELECT location, request_time FROM weather_requests ORDER BY request_time DESC LIMIT 5")
                recent = cursor.fetchall()
                if recent:
                    for loc, time in recent:
                        st.text(f"• {loc} ({time[:10]})")
                else:
                    st.text("No recent searches")

    elif main_choice == "Weather Requests":
        if submenu == "Create Request":
            st.markdown('<h2 class="subheader">Create Weather Request</h2>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    location = st.text_input("Location:", placeholder="Enter city, region, or coordinates")
                
                with col2:
                    time_range = st.selectbox(
                        "Time Range Preset:", 
                        ["Custom Range", "Today", "Next 7 Days", "Next 30 Days"]
                    )
                
                # Handle date selection based on time range
                if time_range == "Custom Range":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_date = st.date_input("Start Date", min_value=datetime.now().date())
                    with col2:
                        end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=7))
                elif time_range == "Today":
                    start_date = end_date = datetime.now().date()
                elif time_range == "Next 7 Days":
                    start_date = datetime.now().date()
                    end_date = start_date + timedelta(days=7)
                elif time_range == "Next 30 Days":
                    start_date = datetime.now().date()
                    end_date = start_date + timedelta(days=30)
                
                # Additional notes (optional)
                notes = st.text_area("Additional Notes (Optional):", max_chars=200)
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    submit = st.button("Save Request", use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if submit and location:
                    with st.spinner("Processing your request..."):
                        success = create_weather_request(
                            location, 
                            start_date.strftime("%Y-%m-%d"), 
                            end_date.strftime("%Y-%m-%d")
                        )
                        
                        if success:
                            st.success(f"Weather request for {location} saved successfully!")
                        else:
                            st.error("Failed to create weather request. Please check your inputs.")

        elif submenu == "View Requests":
            st.markdown('<h2 class="subheader">View Weather Requests</h2>', unsafe_allow_html=True)
            
            # Add search and filter options
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                search = st.text_input("Search by location:", "")
            with col2:
                sort_by = st.selectbox("Sort by:", ["Newest First", "Oldest First", "Temperature (High to Low)", "Temperature (Low to High)"])
            with col3:
                limit = st.slider("Show entries:", 5, 50, 20)
            
            # Build the query based on filters
            query = "SELECT * FROM weather_requests"
            params = []
            
            if search:
                query += " WHERE location LIKE ?"
                params.append(f"%{search}%")
            
            if sort_by == "Newest First":
                query += " ORDER BY request_time DESC"
            elif sort_by == "Oldest First":
                query += " ORDER BY request_time ASC"
            elif sort_by == "Temperature (High to Low)":
                query += " ORDER BY temperature DESC"
            elif sort_by == "Temperature (Low to High)":
                query += " ORDER BY temperature ASC"
            
            query += f" LIMIT {limit}"
            
            # Execute the query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if rows:
                # Convert to DataFrame for better display
                df = pd.DataFrame(rows, columns=["ID", "Location", "Latitude", "Longitude", "Start Date", "End Date", "Temperature", "Description", "Request Time"])
                
                # Format the DataFrame
                df["Temperature"] = df["Temperature"].apply(lambda x: f"{x:.1f}°C")
                df["Description"] = df["Description"].apply(lambda x: x.capitalize())
                df["Request Time"] = df["Request Time"].apply(lambda x: x.split("T")[0])
                
                # Display with highlighting
                st.dataframe(
                    df, 
                    column_config={
                        "ID": st.column_config.NumberColumn("ID", width="small"),
                        "Location": st.column_config.TextColumn("Location", width="medium"),
                        "Temperature": st.column_config.TextColumn("Temp", width="small"),
                        "Description": st.column_config.TextColumn("Weather", width="medium"),
                        "Request Time": st.column_config.DateColumn("Date", width="small", format="YYYY-MM-DD"),
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Pagination placeholder
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.write("showing 1 to", min(limit, len(rows)), "of", len(rows), "entries")
            else:
                st.info("No weather requests found.")

        elif submenu == "Update Request":
            st.markdown('<h2 class="subheader">Update Weather Request</h2>', unsafe_allow_html=True)
            
            # First, let the user select a record
            cursor.execute("SELECT id, location, temperature, weather_desc FROM weather_requests")
            records = cursor.fetchall()
            
            if records:
                record_options = {f"ID: {r[0]} - {r[1]} ({r[2]}°C, {r[3]})": r[0] for r in records}
                
                selected_record = st.selectbox(
                    "Select a record to update:",
                    options=list(record_options.keys())
                )
                
                record_id = record_options[selected_record]
                
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_temp = st.number_input(
                            "New Temperature (°C):", 
                            min_value=-50.0, 
                            max_value=50.0, 
                            step=0.1
                        )
                    with col2:
                        new_desc = st.text_input(
                            "New Weather Description:",
                            placeholder="e.g., sunny, cloudy, rainy"
                        )
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        update_btn = st.button("Update Record", use_container_width=True, key="update_button")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if update_btn:
                        with st.spinner("Updating record..."):
                            success = update_weather_request(
                                record_id, 
                                new_temp if new_temp != 0 else None, 
                                new_desc if new_desc else None
                            )
                            
                            if success:
                                st.success(f"Record ID {record_id} updated successfully!")
                            else:
                                st.error("Failed to update record.")
            else:
                st.info("No records available to update.")

        elif submenu == "Delete Request":
            st.markdown('<h2 class="subheader">Delete Weather Request</h2>', unsafe_allow_html=True)
            
            # Show all records with delete buttons
            cursor.execute("SELECT id, location, start_date, temperature, weather_desc FROM weather_requests")
            records = cursor.fetchall()
            
            if records:
                st.write("Select a record to delete:")
                
                for i, (id, location, date, temp, desc) in enumerate(records):
                    with st.container():
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.write(f"**ID: {id} - {location}** ({date})")
                            st.write(f"Temperature: {temp}°C, {desc}")
                        with cols[1]:
                            if st.button("Delete", key=f"del_{id}", use_container_width=True):
                                with st.spinner("Deleting..."):
                                    success = delete_weather_request(id)
                                    if success:
                                        st.success(f"Record ID {id} deleted successfully!")
                                        st.rerun()  # Refresh the page
                                    else:
                                        st.error("Failed to delete record.")
                        st.divider()
            else:
                st.info("No records available to delete.")

    elif main_choice == "Weather Analysis":
        st.markdown('<h2 class="subheader">Weather Analysis & Trends</h2>', unsafe_allow_html=True)
        
        # Get data for analysis
        cursor.execute("SELECT location, temperature, start_date FROM weather_requests")
        analysis_data = cursor.fetchall()
        
        if analysis_data:
            # Convert to DataFrame
            df = pd.DataFrame(analysis_data, columns=["Location", "Temperature", "Date"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.strftime('%b')
            
            # Create tabs for different visualizations
            tabs = st.tabs(["Temperature Distribution", "Location Analysis", "Time Trends"])
            
            with tabs[0]:
                st.subheader("Temperature Distribution")
                
                # Show histogram of temperatures
                temp_hist_values = df["Temperature"].tolist()
                st.bar_chart(df["Temperature"].value_counts().sort_index())
                
                # Show temperature stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Minimum", f"{df['Temperature'].min():.1f}°C")
                with col2:
                    st.metric("Maximum", f"{df['Temperature'].max():.1f}°C")
                with col3:
                    st.metric("Average", f"{df['Temperature'].mean():.1f}°C")
                with col4:
                    st.metric("Median", f"{df['Temperature'].median():.1f}°C")
            
            with tabs[1]:
                st.subheader("Location Analysis")
                
                # Top locations by count
                location_counts = df["Location"].value_counts().head(10)
                st.bar_chart(location_counts)
                
                # Average temperature by location
                location_temps = df.groupby("Location")["Temperature"].mean().sort_values(ascending=False)
                st.subheader("Average Temperature by Location")
                st.bar_chart(location_temps)
            
            with tabs[2]:
                st.subheader("Time Trends")
                
                # Group by month
                if not df["Month"].empty:
                    monthly_temps = df.groupby("Month")["Temperature"].mean()
                    # Reorder months
                    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    monthly_temps = monthly_temps.reindex(months_order, fill_value=0)
                    
                    st.line_chart(monthly_temps)
        else:
            st.info("Not enough data for analysis. Please create some weather requests first.")

    elif main_choice == "Media & Export":
        if submenu == "YouTube Videos":
            st.markdown('<h2 class="subheader">Weather Videos</h2>', unsafe_allow_html=True)
            
            col1, col_btn = st.columns([3, 1])
            with col1:
                location = st.text_input("Enter location to find weather videos:", placeholder="e.g., London, Tokyo, New York")
            with col_btn:
                search_videos = st.button("Search", use_container_width=True)
            
            if location and search_videos:
                with st.spinner(f"Searching for weather videos about {location}..."):
                    videos = get_youtube_videos(location)
                    
                    if videos:
                        st.success(f"Found {len(videos)} videos about {location} weather!")
                        
                        for i, video in enumerate(videos):
                            with st.container():
                                st.markdown(f"""
                                <div class="youtube-card">
                                    <h3>📺 {video['title']}</h3>
                                    <a href="{video['url']}" target="_blank">{video['url']}</a>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error(f"No videos found for {location}.")

        elif submenu == "Export Data":
            st.markdown('<h2 class="subheader">Export Weather Data</h2>', unsafe_allow_html=True)
            
            # Add export options
            export_format = st.radio("Select export format:", ["CSV", "JSON"])
            
            # Add date range filter
            col1, col2 = st.columns(2)
            with col1:
                date_from = st.date_input("From date:", datetime.now().date() - timedelta(days=30))
            with col2:
                date_to = st.date_input("To date:", datetime.now().date())
            
            # Add location filter
            cursor.execute("SELECT DISTINCT location FROM weather_requests")
            locations = [row[0] for row in cursor.fetchall()]
            
            if locations:
                selected_locations = st.multiselect("Filter by locations:", ["All"] + locations, default=["All"])
                
                if "All" in selected_locations:
                    location_filter = ""
                else:
                    placeholders = ", ".join(["?" for _ in selected_locations])
                    location_filter = f"AND location IN ({placeholders})"
            else:
                location_filter = ""
                selected_locations = []
            
            col1, col2 = st.columns([1, 3])
            with col1:
                export_btn = st.button("Export Data", use_container_width=True)
            
            if export_btn:
                with st.spinner("Preparing export..."):
                    # Build the query
                    query = f"""
                    SELECT * FROM weather_requests 
                    WHERE start_date >= ? AND start_date <= ? 
                    {location_filter}
                    """
                    
                    params = [date_from.strftime("%Y-%m-%d"), date_to.strftime("%Y-%m-%d")]
                    if location_filter and "All" not in selected_locations:
                        params.extend(selected_locations)
                    
                    cursor.execute(query, params)
                    export_data = cursor.fetchall()
                    
                    if export_data:
                        column_names = ["ID", "Location", "Latitude", "Longitude", "Start Date", "End Date", "Temperature", "Weather Description", "Request Time"]
                        df = pd.DataFrame(export_data, columns=column_names)
                        
                        if export_format == "CSV":
                            filename = "weather_data_export.csv"
                            df.to_csv(filename, index=False)
                            
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="Download CSV",
                                    data=file,
                                    file_name=filename,
                                    mime="text/csv",
                                    key="download-csv"
                                )
                        else:  # JSON
                            filename = "weather_data_export.json"
                            df.to_json(filename, orient="records", date_format="iso")
                            
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="Download JSON",
                                    data=file,
                                    file_name=filename,
                                    mime="application/json",
                                    key="download-json"
                                )
                        
                        st.success(f"Export complete! {len(export_data)} records exported.")
                    else:
                        st.warning("No data found matching your criteria.")

if __name__ == "__main__":
    main()