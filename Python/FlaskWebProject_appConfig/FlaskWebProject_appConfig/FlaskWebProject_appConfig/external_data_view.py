from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup

external_data_bp = Blueprint('external_data', __name__)

@external_data_bp.route('/external_data')
def external_data():
    url = 'https://www.nseindia.com/market-data/live-market-indices'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table data
        table = soup.find('table', {'class': 'live-market-indices-table'})
        rows = table.find_all('tr')
        
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        data = []
    
    return render_template('external_data.html', data=data)