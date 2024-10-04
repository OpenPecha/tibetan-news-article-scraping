import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin





def extract_all_tbwriters_article_links(url):
    """
    Extracts all article links from a given tbwriters webpage.

    Args:
    url (str): The URL of the tbwriters webpage containing article links.

    Returns:
    Dict[str, Any]: A dictionary containing article links and status details.
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    final_response = {
        "Links": [],
        "Message": "Success",
        "Response": 200,
        "source_url": url
    }
    load_more = False
    
    try:
        start_time = time.time()
        # response = requests.get(url, headers=headers, timeout=(5, 60-5))
        response = requests.get(url, headers=headers,)
        response.raise_for_status()
        end_time = time.time()
        if end_time - start_time > 200:
            print(f"This URL took more than 50s: {url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        article_div = soup.find("div", class_="wrapper section medium-padding")
        if not article_div:
            raise ValueError("Could not find the main article container on the page.")
        
        all_articles = article_div.find_all("div", class_="post-container")
        if not all_articles:
            raise ValueError("Could not find the each article container on the page.")
        article_links = []
        for article in all_articles:
            # 
            title_Link = article.find("div", class_="post-header")
            if title_Link:
                links = title_Link.find("a")
                if links.get("href"):
                    article_links.append(links.get("href"))
        
        final_response["Links"] = article_links
        load_more_span = soup.find("div", class_="archive-nav section-inner")
        if load_more_span:
            load_more = load_more_span.find("a", class_="post-nav-older fleft")
            if load_more:
                load_more = True
            else:
                load_more = False

        return final_response, load_more
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
        return final_response, True
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response, True
    except ValueError as e:
        final_response["Message"] = f"An error occurred while parsing the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response, True
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response, True











import requests
from bs4 import BeautifulSoup
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def scrape_tbwriters_article_content(url, tags):
    """
    
    
    """


    
    headers = {
        "authority": "www.tbwriters.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "referer": "https://www.tbwriters.com/?paged=3",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "", "Text": []},
            'meta_data': {'URL': url, 'Author': "", 'Date': "", 'Tags': [tags]}
        },
        "Message": "Success",
        "Response": 200
    }
    
    try:
        time.sleep(random.uniform(1, 3))
        
        session = requests_retry_session()
        response = session.get(url, headers=headers, allow_redirects=True)
        
        if response.status_code == 304:
            # If we get a 304, try again without any caching headers
            headers.pop('If-Modified-Since', None)
            headers.pop('If-None-Match', None)
            response = session.get(url, headers=headers, allow_redirects=True)
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Soup content length: {len(str(soup))}")  # Debug print
        
        title_block = soup.find("h1", class_="post-title")
        if title_block:
            # Extract title
            title = soup.find('a', rel='bookmark').text.strip()
            
            # Extract date
            date_text = soup.find('h1', class_='post-title').contents[-1].strip()
            date = date_text.split('སྤེལ་དུས།')[-1].strip()
            final_response['data']["title"] = title
            final_response['data']['meta_data']["Date"] = date
            
        author_block = soup.find("div", class_="post-author-content")
        if author_block:
            author_para = author_block.find("p")
            if author_para:
                author = author_para.get_text(strip=True)
                final_response['data']['meta_data']["Author"] = author


            
        body = soup.find("div", class_="post-content")
        if body:
            text = body.get_text(separator='\n', strip=True)
            lines = [line for line in text.split('\n') if line.strip()]
            if lines:
                final_response['data']['body']["Text"] = lines
            else:
                final_response['data']['body']["Text"] = [""]                    
        else:
            final_response['data']['body']["Text"] = [""]
        
        return final_response
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the article: {str(e)}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {str(e)}"
        final_response["Response"] = 500
    
    return final_response




