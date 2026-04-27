import requests
import json
import pandas as pd
import sqlite3

# Please replace 'YOUR_AUTHORIZATION_KEY' with your actual CWA API authorization key
# You can get it from the CWA API Portal: https://opendata.cwa.gov.tw/
API_KEY = 'CWA-77A0C3C8-E800-4830-996A-190BE56C4EF1'

# Dataset ID for 一週天氣預報 (台灣未來1週天氣預報)
DATASET_ID = 'F-D0047-091' 

# Regions specified: 台灣北部、中部、南部、東北部、東部及東南部地區 (Basically almost all regions, we will fetch the whole dataset and filter/display)
url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/{DATASET_ID}?Authorization={API_KEY}&format=JSON'

def fetch_weather_data():
    try:
        print("Fetching data from CWA API...")
        response = requests.get(url)
        
        # If unauthorized, it might return 401. Let's handle it gracefully.
        if response.status_code == 401:
            print("Error: Unauthorized. Please check your API_KEY.")
            return

        response.raise_for_status() # Check if the request was successful
        data = response.json()
        
        # Using json.dumps to observe the JSON output as requested
        print("=== Raw JSON Output (First 1000 characters) ===")
        print(json.dumps(data, indent=4, ensure_ascii=False)[:1000])
        print("...\n")

        # Parsing the data
        if 'records' in data and 'Locations' in data['records']:
            locations = data['records']['Locations'][0]['Location']
            parsed_data = []
            
            for loc in locations:
                location_name = loc.get('LocationName')
                weather_elements = loc.get('WeatherElement', [])
                
                # Extracting basic info like Wx (Weather condition), T (Temperature)
                for element in weather_elements:
                    element_name = element.get('ElementName')
                    if element_name in ['天氣現象', '最高溫度', '最低溫度', '12小時降雨機率']:
                        times = element.get('Time', [])
                        for t in times:
                            start_time = t.get('StartTime')
                            end_time = t.get('EndTime')
                            element_value = t.get('ElementValue', [{}])[0]
                            param_name = list(element_value.values())[0] if element_value else ''
                            
                            parsed_data.append({
                                'Location': location_name,
                                'Element': element_name,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Value': param_name
                            })
            
            # Using pandas to display the parsed data nicely
            df = pd.DataFrame(parsed_data)
            print("=== Parsed Data (Pandas DataFrame) ===")
            print(df.head(20)) # Print the first 20 rows for preview
            
            # Save to CSV
            df.to_csv('weather_data.csv', index=False, encoding='utf-8-sig')
            print(f"\nData saved to weather_data.csv ({len(df)} rows)")
            
            # Save to SQLite3
            conn = sqlite3.connect('weather_data.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_forecast (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT,
                    element TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    value TEXT,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Clear old data and insert fresh
            cursor.execute('DELETE FROM weather_forecast')
            for _, row in df.iterrows():
                cursor.execute(
                    'INSERT INTO weather_forecast (location, element, start_time, end_time, value) VALUES (?, ?, ?, ?, ?)',
                    (row['Location'], row['Element'], row['Start Time'], row['End Time'], row['Value'])
                )
            conn.commit()
            print(f"Data saved to weather_data.db (SQLite3, {len(df)} rows)")
            
            # Verify: query and display sample
            cursor.execute('SELECT location, element, start_time, value FROM weather_forecast LIMIT 5')
            print("\n=== SQLite3 Sample Query ===")
            for r in cursor.fetchall():
                print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")
            conn.close()

        else:
            print("Data structure is different from expected or no records found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    if API_KEY == 'YOUR_AUTHORIZATION_KEY':
        print("WARNING: Please set your API_KEY in the script before running.")
    else:
        fetch_weather_data()
