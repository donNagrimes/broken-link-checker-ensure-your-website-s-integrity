thonimport requests
import logging

def validate_link(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logging.warning(f"Broken link detected: {url} - Status: {response.status_code}")
            return {
                'url': url,
                'httpStatus': response.status_code,
                'title': "N/A",
                'referrer': "N/A"
            }
        return None
    except requests.RequestException as e:
        logging.error(f"Error validating {url}: {e}")
        return None