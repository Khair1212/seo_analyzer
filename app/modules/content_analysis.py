import requests
from bs4 import BeautifulSoup
from logger import logger

def analyze(url):
    logger.info(f"Analyzing content for {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else None
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_description['content'] if meta_description else None
    
    h1_tags = [h1.text for h1 in soup.find_all('h1')]
    img_alt_texts = [img.get('alt', '') for img in soup.find_all('img')]
    
    content = ' '.join([p.text for p in soup.find_all('p')])
    word_count = len(content.split())
    
    return {
        'title': title,
        'meta_description': meta_description,
        'h1_tags': h1_tags,
        'img_alt_texts': img_alt_texts,
        'word_count': word_count
    }