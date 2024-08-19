import requests
from bs4 import BeautifulSoup

def scrape_vot_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1', class_='tdb-title-text')
        title_text = title.text.strip() if title else "Title not found"

        # Extracting Meta Data
        meta_data_body = soup.find('div', class_="vc_column_inner tdi_85 wpb_column vc_column_container tdc-inner-column td-pb-span6")
        author_name = meta_data_body.find('a', class_="tdb-author-name").get_text() if meta_data_body else "Author not found"
        date_time_meta = meta_data_body.find('time', class_="entry-date updated td-module-date").get_text() if meta_data_body else "Date not found"
        website_meta = url

        meta_data = {
            "Author": author_name,
            "Date": date_time_meta,
            "URL": website_meta
        }

        # Extract body content
        body = soup.find('div', class_='td_block_wrap tdb_single_content tdi_100 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
        if body:
            # Extracting all <p> tags for text content
            paragraphs = body.find_all('p')
            text_content = [para.get_text(strip=True) for para in paragraphs]

            # Find the audio tag and get its src attribute
            audio = body.find('figure', class_='wp-block-audio')
            audio_tag = audio.find('audio') if audio else None
            audio_src = audio_tag.get('src') if audio_tag else "No audio tag found"

            body_text = {
                "Audio": audio_src,
                "Text": text_content
            }
        else:
            body_text = "Body content not found"
        
        return {
            'title': title_text,
            'body': body_text,
            'meta_data': meta_data
        }
    except requests.RequestException as e:
        return {
            'title': "Error",
            'body': f"An error occurred while fetching the article: {str(e)}",
            'meta_data': {'URL': url}
        }

# List of article URLs
urls = [
    "https://vot.org/%e0%bc%b8%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b%e0%bd%98%e0%bd%86%e0%bd%bc%e0%bd%82%e0%bc%8b%e0%bd%82%e0%bd%b2%e0%bd%a6%e0%bc%8b-swiss-%e0%bd%91%e0%bd%84%e0%bc%8b-liechtenstein/",
    "https://vot.org/%e0%bd%a8%e0%bc%8b%e0%bd%a2%e0%bd%b2%e0%bd%a0%e0%bd%b2%e0%bc%8b%e0%bd%93%e0%bd%b2%e0%bd%a0%e0%bd%b4%e0%bc%8b%e0%bd%a1%e0%bd%bc%e0%bd%82%e0%bc%8b%e0%bd%82%e0%bd%b2%e0%bc%8b-ubs-arena-%e0%bd%a2/",
    "https://vot.org/vot%e0%bd%82%e0%bd%84%e0%bd%a6%e0%bd%98%e0%bd%86%e0%bd%82%e0%bd%a3%e0%bd%96%e0%bd%a2%e0%bd%93%e0%bd%96%e0%bd%9e-2/",
    "https://vot.org/wisdom-of-happiness-%e0%bd%9e%e0%bd%ba%e0%bd%a6%e0%bc%8b%e0%bc%b8%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b%e0%bd%98%e0%bd%86%e0%bd%bc%e0%bd%82%e0%bc%8b%e0%bd%91%e0%bd%84%e0%bc%8b%e0%bd%a0/",
    "https://vot.org/vott%e0%bd%82%e0%bd%84%e0%bd%a6%e0%bd%98%e0%bd%86%e0%bd%82%e0%bd%82%e0%bd%a6%e0%bd%80%e0%bd%a2/",
    "https://vot.org/vott%e0%bd%82%e0%bd%84%e0%bd%a6%e0%bd%98%e0%bd%86%e0%bd%82%e0%bd%82%e0%bd%a6%e0%bd%a6%e0%bd%91%e0%bd%a6-3/",
    "https://vot.org/%e0%bc%b8%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b%e0%bd%98%e0%bd%86%e0%bd%bc%e0%bd%82%e0%bc%8b%e0%bd%82%e0%bd%b2%e0%bc%8b%e0%bd%9e%e0%bd%96%e0%bd%a6%e0%bc%8b%e0%bd%94%e0%bd%b4%e0%bd%a6-2/",
    "https://vot.org/%e0%bd%a2%e0%be%92%e0%be%b1%e0%bc%8b%e0%bd%82%e0%bd%a2%e0%bc%8b%e0%bd%82%e0%bd%9e%e0%bd%b4%e0%bd%84%e0%bc%8b%e0%bd%93%e0%bd%a6%e0%bc%8b%e0%bc%b8%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b-3/",
    "https://vot.org/vot%e0%bd%96%e0%bd%a3%e0%bd%a1%e0%bd%a3%e0%bd%91%e0%bd%a6%e0%bd%a0%e0%bd%a0%e0%bd%81%e0%bd%84/"
]

# Process each URL
for url in urls:
    article = scrape_vot_article(url)
    
    # Print the article details
    print("Title:", article['title'])
    print("Author:", article['meta_data'].get('Author', 'N/A'))
    print("Date:", article['meta_data'].get('Date', 'N/A'))
    print("URL:", article['meta_data'].get('URL', 'N/A'))

    if isinstance(article['body'], dict):
        text = ' '.join(article['body'].get('Text', []))
        audio = article['body'].get('Audio', 'None')
    else:
        text = article['body']
        audio = 'None'

    print("Text:", text)
    print("Audio:", audio)
    print("\n" + "-"*40 + "\n")
