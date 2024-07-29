import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import shutil

def get_chrome_history():
    # Path to the Chrome history database
    data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
    history_db = os.path.join(data_path, 'History')

    # Make a copy of the history database
    temp_history_db = os.path.join(data_path, 'temp_History')
    shutil.copy2(history_db, temp_history_db)

    # Connect to the copied database
    conn = sqlite3.connect(temp_history_db)
    cursor = conn.cursor()

    # Query to retrieve history data
    cursor.execute("""
    SELECT urls.url, urls.title, urls.visit_count, urls.last_visit_time
    FROM urls
    ORDER BY last_visit_time DESC
    LIMIT 20
    """)

    # Create a DataFrame from the results
    columns = ['url', 'title', 'visit_count', 'last_visit_time']
    df = pd.DataFrame(cursor.fetchall(), columns=columns)

    # Convert the last_visit_time to a readable format and adjust for IST
    def convert_to_ist(utc_time):
        epoch_start = datetime(1601, 1, 1)
        utc_time = epoch_start + timedelta(microseconds=utc_time)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')

    df['last_visit_time'] = df['last_visit_time'].apply(convert_to_ist)

    # Close the database connection
    conn.close()

    # Remove the copied database file
    os.remove(temp_history_db)

    return df

# Get the history data
history_df = get_chrome_history()
history_df.to_csv('chrome_history.csv', index=False)
print(history_df)
