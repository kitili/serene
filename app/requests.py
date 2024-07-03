import requests
from flask import current_app

def get_quotes():
    try:
        url = current_app.config.get('QUOTES_API_BASE_URL')
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        if response.text:
            return response.json()
        else:
            current_app.logger.warning("Empty response from quotes API")
            return None
    except requests.RequestException as e:
        current_app.logger.error(f"Error fetching quotes: {str(e)}")
        return None
    except ValueError as e:
        current_app.logger.error(f"Error parsing JSON from quotes API: {str(e)}")
        return None