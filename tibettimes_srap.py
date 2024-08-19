import requests
from bs4 import BeautifulSoup
import json
import time

def extract_article_links(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Modify this according to the actual HTML structure
        article_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/article/' in href:  # Adjust the condition to match article links
                article_links.append(href)
        
        return article_links
    
    except requests.RequestException as e:
        print(f"Error fetching page {page_url}: {e}")
        return []

def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1')  # Adjust for actual title tag
        title_text = title.get_text(strip=True) if title else "Title not found"

        body = soup.find('div', class_='jeg_post_content')  # Adjust based on actual class
        text_content = []
        author = "Author not found"
        date = "Date not found"
        audio_src = "No audio found"

        if body:
            paragraphs = body.find_all('p')
            for paragraph in paragraphs:
                text_content.append(paragraph.get_text(strip=True))

            meta_data = soup.find('div', class_='jeg_post_meta')
            if meta_data:
                author_tag = meta_data.find('div', class_='by')
                date_tag = meta_data.find('time', class_='entry-date')
                audio_tag = body.find('figure', class_='wp-block-audio')

                author = author_tag.get_text(strip=True) if author_tag else "Author not found"
                date = date_tag.get_text(strip=True) if date_tag else "Date not found"
                
                if audio_tag:
                    audio = audio_tag.find('audio')
                    audio_src = audio.get('src') if audio else "No audio source found"
        
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

def scrape_multiple_pages(base_url, num_pages, articles_per_page):
    all_articles = []

    for page_number in range(1, num_pages + 1):
        page_url = f"{base_url}/{page_number}/"
        print(f"Extracting links from {page_url}...")
        article_links = extract_article_links(page_url)
        
        if not article_links:
            print(f"No articles found on {page_url}")
            continue
        
        # Ensure only the required number of articles per page
        article_links = article_links[:articles_per_page]

        for link in article_links:
            print(f"Scraping article {link}...")
            article = scrape_article(link)
            all_articles.append(article)
            time.sleep(1)  # Delay to respect the website's server load
    
    # Save all articles to a JSON file
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print("All article data has been saved to 'articles.json'")

# Usage
base_url = "https://tibettimes.net/category/news/dalai-lama/page"
num_pages = 10  # Number of pages to scrape
articles_per_page = 8  # Number of articles to scrape per page
scrape_multiple_pages(base_url, num_pages, articles_per_page)
