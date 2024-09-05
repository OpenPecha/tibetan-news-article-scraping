import requests
from bs4 import BeautifulSoup
import json

def scrape_tt_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h3')
        title_text = title.get_text(strip=True) if title else "Title not found"

        # Locate the main content container
        body = soup.find('div', class_='jeg_post_excerpt') # content-inner
        
        # Initialize variables for content
        text_content = []
        author = "Author not found"
        date = "Date not found"
        audio_src = "No audio found"

        if body:
            # Extract all <span> tags within the main content container
            spans = body.find_all('span')
            
            # Iterate through the spans and extract text
            for span in spans:
                text_content.append(span.get_text(strip=True))

            # Extract author and date from meta-data if available
            meta_data = soup.find('div', class_='jeg_post_meta')
            if meta_data:
                author_tag = meta_data.find('span', class_='by')
                date_tag = meta_data.find('time', class_='entry-date')
                audio_tag = body.find('figure', class_='wp-block-audio')
                
                author = author_tag.get_text(strip=True) if author_tag else "Author not found"
                date = date_tag.get_text(strip=True) if date_tag else "Date not found"
                
                if audio_tag:
                    audio = audio_tag.find('audio')
                    audio_src = audio.get('src') if audio else "No audio source found"
        
        # Return the structured result
        return {
            'title': title_text,
            'text': '\n'.join(text_content) if text_content else "No text content found",
            'meta_data': {
                'author': author,
                'date': date,
                'audio': audio_src
            }
        }
    
    except requests.RequestException as e:
        return {
            'title': "Error",
            'text': f"An error occurred while fetching the article: {str(e)}",
            'meta_data': {'author': "Unknown", 'date': "Unknown", 'audio': "None"}
        }

def scrape_multiple_articles(base_url, num_articles):
    articles = []
    for i in range(1, num_articles + 1):
        # Generate the URL for each article (assuming a pattern in URL)
        url = f"{base_url}/{i}/"
        print(f"Scraping {url}...")
        article = scrape_tt_article(url)
        articles.append(article)
    
    # Saving to a JSON file
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    
    print("All article data has been saved to 'articles.json'")

# Usage
base_url = "https://tibettimes.net/category/news/dalai-lama/page/"
num_articles = 10  # Specify the number of articles to scrape
scrape_multiple_articles(base_url, num_articles)
