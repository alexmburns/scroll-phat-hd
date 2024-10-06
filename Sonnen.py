import requests
import time
import scrollphathd
from scrollphathd.fonts import font3x5  # Import the 3x5 font

# Local API URL for your Sonnen system
API_URL = "http://192.168.0.3/api/v1/status"
ACCESS_TOKEN = ""  # Your Sonnen API key

# Function to get Sonnen data
def get_sonnen_data():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',  # Use the provided API key
    }
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses
        return response.json()  # Return the API data as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to display one piece of data on Scroll pHAT HD
def display_message(message):
    scrollphathd.clear()
    scrollphathd.write_string(message, x=0, y=0, font=font3x5, brightness=0.5)
    scrollphathd.show()
    
    # Flip the entire display buffer 180 degrees
    scrollphathd.rotate(180)  # This rotates the buffer
    scrollphathd.show()
    time.sleep(2)  # Pause for 2 seconds to show the message

# Function to safely get a numerical value and convert watts to kilowatts
def get_kw_value(value):
    try:
        if isinstance(value, (int, float)):  # Ensure the value is a number
            return f"{abs(value) / 1000:.1f}kW" if value != 0 else "0.0kW"  # Use abs() to remove the minus sign
        else:
            return "N/A"
    except Exception:
        return "N/A"  # Handle any errors quietly

# Function to display Sonnen data
def display_sonnen_data(data):
    # Extracting the necessary values with safe fallbacks
    battery_charge = str(data.get('USOC', 'N/A'))  # Battery charge percentage
    production_kw = get_kw_value(data.get('Production_W', 0))  # Power currently produced (in kilowatts)
    consumption_kw = get_kw_value(data.get('Consumption_W', 0))  # Power currently being consumed (in kilowatts)

    # Handle negative values for grid power
    grid_feed_in = data.get('GridFeedIn_W', 0)
    grid_kw = f"{abs(grid_feed_in) / 1000:.1f}kW" if grid_feed_in != 0 else "0.0kW"  # Use abs() to remove the minus sign

    # Define the pages to display - each label followed by its value
    pages = [
        ("Batt", f"{battery_charge}%"),
        ("Sun", production_kw),
        ("Use", consumption_kw),
        ("Grid", grid_kw)
    ]

    # Start cycling through pages
    while True:
        for label, value in pages:
            # Display the label for 2 seconds
            display_message(label)

            # Display the value for 2 seconds
            display_message(value)

# Main loop
while True:
    data = get_sonnen_data()
    if data:
        display_sonnen_data(data)

    # Refresh every 60 seconds (no additional pause before refreshing the cycle)
    time.sleep(60)
