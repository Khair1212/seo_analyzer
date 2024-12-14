import requests
from urllib.parse import urlparse
from logger import logger

def analyze(url):
    logger.info(f"Analyzing technical SEO for {url}")
    parsed_url = urlparse(url)
    is_https = parsed_url.scheme == 'https'
    
    response = requests.get(url)
    headers = response.headers
    
    has_robots_txt = requests.get(f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt").status_code == 200
    has_sitemap = requests.get(f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml").status_code == 200
    
    return {
        'is_https': is_https,
        'server': headers.get('Server'),
        'has_robots_txt': has_robots_txt,
        'has_sitemap': has_sitemap,
        'status_code': response.status_code
    }