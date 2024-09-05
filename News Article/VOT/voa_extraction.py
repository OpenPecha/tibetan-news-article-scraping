import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import time

def extract_all_article(url: str):
    """
    Extracts all article links from a given VOT (Voice of Tibet) webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the VOT webpage containing article links.

    Returns:
        {
            "Links": List[],
            "Message": string,
            "Response": int
        }
    Raises:
    requests.RequestException: If there's an error fetching the webpage.
    ValueError: If the expected HTML structure is not found on the page.
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
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=(5, 60-5))
        response.raise_for_status()
        end_time = time.time()
        if end_time-start_time > 50:
            print(f"This ULR Took more then 50s: {url}")
            
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting all the articles in the DIV
        all_article = soup.find("div", class_="td_block_inner tdb-block-inner td-fix-index")
        if not all_article:
            raise ValueError("Could not find the main article container on the page.")
        
        # Getting all the links of articles 
        article_links = all_article.find_all("a", class_="td-image-wrap")
        all_links = [link.get("href") for link in article_links if link.get("href")]
        final_response["Links"] = all_links
        return final_response
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408  # Request Timeout
        return final_response
    except requests.RequestException as e:
        # print(f"An error occurred while fetching the webpage: {e}")
        final_response["Message"] = f"An error occurred while fetching the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', None)
        return final_response
    except ValueError as e:
        # print(f"An error occurred while parsing the webpage: {e}")
        final_response["Message"] = f"An error occurred while parsing the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', None)
        return final_response
    except Exception as e:
        # print(f"An unexpected error occurred: {e}")
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response




def scrape_vot_article(url: str) -> Dict[str, Any]:
    """
    Scrapes an article from the VOT (Voice of Tibet) website.

    Args:
    url (str): The URL of the VOT article to scrape.

    Returns:
    Dict[str, Any]: A dictionary containing the scraped information and status details:
        {
            'data': {
                'title': str,
                'body': {
                    'Audio': str,
                    'Text': List[str]
                },
                'meta_data': {
                    'Author': str,
                    'Date': str,
                    'Tags': List[str],
                    'URL': str
                }
            },
            'Message': str,
            'Response': int
        }
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
        title = soup.find('h1', class_='tdb-title-text')
        final_response['data']['title'] = title.text.strip() if title else "Title not found"

        # Extracting Meta Data
        try:
            meta_data_body = soup.find('div', class_="vc_column_inner tdi_85 wpb_column vc_column_container tdc-inner-column td-pb-span6")
            if meta_data_body:
                author_name = meta_data_body.find('a', class_="tdb-author-name")
                final_response['data']['meta_data']["Author"] = author_name.get_text() if author_name else "Author not found"
                
                date_time = meta_data_body.find('time', class_="entry-date updated td-module-date")
                final_response['data']['meta_data']["Date"] = date_time.get_text() if date_time else "Date not found"
        except AttributeError:
            final_response['data']['meta_data']["Author"] = "Error fetching author"
            final_response['data']['meta_data']["Date"] = "Error fetching date"

        # Getting tag meta data 
        try:
            tag_meta = soup.find('ul', class_='tdb-tags')
            if tag_meta:
                tag_meta = tag_meta.select('li a')
                final_response['data']['meta_data']["Tags"] = [tag.text for tag in tag_meta]
        except AttributeError:
            final_response['data']['meta_data']["Tags"] = []

        # Extract body content
        try:
            body = soup.find('div', class_='td_block_wrap tdb_single_content tdi_100 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            if body:
                # Extracting all <p> tags for text content
                paragraphs = body.find_all('p')
                final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]

                # Find the audio tag and get its src attribute
                audio = body.find('figure', class_='wp-block-audio')
                if audio:
                    audio_tag = audio.find('audio')
                    if audio_tag:
                        final_response['data']['body']["Audio"] = audio_tag.get('src', "No audio source found")
        except AttributeError:
            final_response['data']['body']["Text"] = ["Error fetching body content"]
        
        return final_response
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408  # Request Timeout
        return final_response
        
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the article: {str(e)}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response
