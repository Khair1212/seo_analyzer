import requests
from fastapi import HTTPException
from config import PAGESPEED_API_KEY
from logger import logger

def get_insights(url):
    logger.info(f"Fetching PageSpeed Insights for {url}")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={PAGESPEED_API_KEY}"
    response = requests.get(api_url)
    if response.status_code != 200:
        logger.error(f"Failed to fetch PageSpeed Insights: {response.status_code}")
        raise HTTPException(status_code=400, detail="Failed to fetch PageSpeed Insights")
    data = response.json()
    return {
        'performance_score': data['lighthouseResult']['categories']['performance']['score'],
        'opportunities': data['lighthouseResult']['audits']
    }