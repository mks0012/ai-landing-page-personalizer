import requests
from bs4 import BeautifulSoup

def scrape_landing_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        
        if response.status_code != 200:
            return None 

        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        h1 = soup.find('h1').get_text(strip=True)[:100] if soup.find('h1') else "No Headline Found"
        
        
        cta_element = soup.find(['button', 'a'], class_=lambda x: x and 'btn' in x.lower())
        cta = cta_element.get_text(strip=True)[:30] if cta_element else "Sign Up"
        
        return {"h1": h1, "cta": cta}
    except Exception:
        return None