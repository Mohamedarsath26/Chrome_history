from flask import Flask, render_template
import pandas as pd
from history import get_chrome_history

history_df = get_chrome_history()
history_df.to_csv('chrome_history.csv', index=False)

app = Flask(__name__)

@app.route('/')
def home():
    # Read the Chrome history data from CSV
    df = pd.read_csv('chrome_history.csv')
    # Convert the DataFrame to a list of dictionaries
    history_data = df.to_dict(orient='records')
    return render_template('index.html', history=history_data)

if __name__ == '__main__':
    app.run(debug=True)
