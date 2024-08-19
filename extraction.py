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
        author_name = meta_data_body.find('a', class_="tdb-author-name").get_text()
        date_time_meta = meta_data_body.find('time', class_="entry-date updated td-module-date").get_text()
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
            # Getting the text from each <p> tag
            text_content=[]
            for para in paragraphs:
                text_content.append(para.get_text(strip=True))

            # Audio Example:
            # <figure class="wp-block-audio">
            # <audio controls="" src="https://vot.org/wp-content/uploads/2024/08/Gangtok-TYC-54-Working-Committee-Meet-Concludes.mp3">
            # </audio></figure>
            # Find the audio tag and get its src attribute
            audio = body.find('figure', class_='wp-block-audio')
            audio_tag = audio.find('audio')
            if audio_tag:
                audio_src = audio_tag.get('src')
            else:
                audio_src = "No audio tag found"
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

# Usage
url = "https://vot.org/%e0%bc%b8%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b%e0%bd%98%e0%bd%86%e0%bd%bc%e0%bd%82%e0%bc%8b%e0%bd%82%e0%bd%b2%e0%bd%a6%e0%bc%8b-swiss-%e0%bd%91%e0%bd%84%e0%bc%8b-liechtenstein/"
article = scrape_vot_article(url)

print(article)
