import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def extract_article_links_from_page(url: str) -> Dict[str, Any]:
    """
    Extracts article links from a Bangchen page.
    
    Args:
    url (str): The URL of the Bangchen page containing article links.
    
    Returns:
    Dict[str, Any]: A dictionary with:
        - "Links": A list of article URLs.
        - "Message": Status message.
        - "Response": HTTP response code.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    final_response = {
        "Links": [],
        "Message": "Success",
        "Response": 200
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=(5, 60))
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
  
        article_containers = soup.find_all('div', class_='content-area')
        
        if not article_containers:
            raise ValueError("Could not find the article containers on the page.")
        
        article_links = [container.find('a')['href'] for container in article_containers if container.find('a')]
        final_response["Links"] = article_links
        
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
    except ValueError as e:
        final_response["Message"] = str(e)
        final_response["Response"] = 500
        
    return final_response

def scrape_article_details(url: str) -> Dict[str, Any]:
    """
    Scrapes details of an article from Bangchen.
    
    Args:
    url (str): The URL of the Bangchen article to scrape.
    
    Returns:
    Dict[str, Any]: A dictionary with:
        - 'data': Contains title, body content, and meta-data.
        - 'Message': Status message.
        - 'Response': HTTP response code.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "", "Text": []},
            'meta_data': {'URL': url, 'Author': "", 'Date': "", 'Tags': []}
        },
        "Message": "Success",
        "Response": 200
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=120)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h2', class_='entry-title') 
        final_response['data']['title'] = title.text.strip() if title else "Title not found"

        # Extract Meta Data
        author = soup.find('i', class_='far fa-user-circle"')  
        date = soup.find('i', class_='far fa-clock') 
        final_response['data']['meta_data']['Author'] = author.text.strip() if author else "Author not found"
        final_response['data']['meta_data']['Date'] = date.text.strip() if date else "Date not found"
        
        # Extract Body Content
        body = soup.find('div', class_='entry-content') 
        if body:
            paragraphs = body.find_all('p')
            final_response['data']['body']['Text'] = [para.get_text(strip=True) for para in paragraphs]
            
            audio = body.find('audio')
            if audio:
                final_response['data']['body']['Audio'] = audio.get('src', "Audio files are not available on Bangchen")
        
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the article: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        
    return final_response

def fetch_all_article_links(base_url: str, num_pages: int, articles_per_page: int) -> List[str]:
    """
    Fetches article links from multiple pages of the Bangchen category.
    
    Args:
    base_url (str): The base URL of the Bangchen category.
    num_pages (int): The number of pages to scrape.
    articles_per_page (int): Number of articles per page.
    
    Returns:
    List[str]: A list of article URLs.
    """
    all_article_links = []
    for page in range(num_pages):
        url = f"{base_url}?start={page * articles_per_page}"
        response = extract_article_links_from_page(url)
        if response["Response"] == 200:
            all_article_links.extend(response["Links"])
        else:
            print(f"Failed to fetch links from page {page + 1}: {response['Message']}")
    return all_article_links

# usage
category_url = "https://bangchen.tibetexpress.net/category/news/"
# Parameters
start_index = 0
num_pages = 1618
articles_per_page = 10

# Fetch and scrape all articles
all_article_links = fetch_all_article_links(category_url, num_pages, articles_per_page)
for article_url in all_article_links:
    article_data = scrape_article_details(article_url)
    print(article_data)
