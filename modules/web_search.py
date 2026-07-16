from googlesearch import search
import requests
from bs4 import BeautifulSoup

class WebSearch:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search(self, query, num_results=5):
        """Search the web using Google"""
        try:
            results = []
            
            for url in search(query, num_results=num_results, lang='en'):
                results.append({
                    'url': url,
                    'title': self.get_page_title(url)
                })
            
            return results
        
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def get_page_title(self, url):
        """Get the title of a webpage"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.title.string if soup.title else url
        except:
            return url
    
    def get_page_summary(self, url):
        """Get a summary of a webpage"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to get meta description
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta:
                return meta.get('content', '')
            
            # Fallback: get first paragraph
            paragraphs = soup.find_all('p')
            if paragraphs:
                return paragraphs[0].get_text()[:200] + "..."
            
            return "No summary available"
        
        except Exception as e:
            return f"Error: {str(e)}"