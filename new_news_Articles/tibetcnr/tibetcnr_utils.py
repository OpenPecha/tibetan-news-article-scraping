import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin





def extract_tibetcnr_page_article_links(url, base_url):
    """
    Extracts all article links from a given tibetcnr webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the tibetcnr webpage containing article links.

    Returns:
        {
            "Links": List[],
            "Message": string,
            "Response": int,
            "source_url": string
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
        "Response": 200,
        "source_url": url
    }
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=(5, 60-5))
        response.raise_for_status()
        end_time = time.time()

        if end_time-start_time > 50:
            print(f"This ULR Took more then 50s: {url}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # # Getting all the links of articles 
        all_links = []
        all_link_article = soup.find("div", class_="centre2")
        if all_link_article:
            article_content = all_link_article.find("div", class_="content")
            if article_content:
                
                article_block = article_content.find_all("h3", class_="ellipsis")
                if article_block:
                    for each_head in article_block:
                        article_links = each_head.find("a")
                        if article_links:
                            full_url = article_links.get("href")
                            full_url = urljoin(base_url, full_url)
                            all_links.append(full_url)
                        
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
        final_response["Response"] = 404
        # getattr(e.response, 'status_code', None)
        return final_response
    except Exception as e:
        # print(f"An unexpected error occurred: {e}")
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response









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

def scrape_tibetcnr_article_content(url, tags):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'HttpOnly=true; HttpOnly=true',
        'Host': 'www.tibetcnr.com',
        'If-Modified-Since': 'Wed, 04 Sep 2024 01:30:42 GMT',
        'If-None-Match': 'W/"66d7b842-9c57"',
        'Referer': 'http://www.tibetcnr.com/zdgz2019/index_1.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
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
        
        # Custom redirect handling
        redirect_count = 0
        max_redirects = 10
        while redirect_count < max_redirects:
            response = session.get(url, headers=headers, allow_redirects=False, timeout=30)
            
            if response.status_code in (301, 302, 303, 307, 308):
                url = response.headers['Location']
                redirect_count += 1
                print(f"Redirect {redirect_count}: {url}")
            else:
                break
        
        if redirect_count == max_redirects:
            raise requests.TooManyRedirects(f"Exceeded {max_redirects} redirects")
        
        if response.status_code == 304:
            headers.pop('If-Modified-Since', None)
            headers.pop('If-None-Match', None)
            response = session.get(url, headers=headers, allow_redirects=False, timeout=30)
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tags_body = soup.find("div", class_="tag")
        if tags_body:
            final_response['data']['meta_data']["Tags"] = tags_body.get_text(strip=True)
        
        full_body = soup.find('div', class_="article")
        if full_body:
            title = full_body.find('h2')
            if title:
                final_response['data']["title"] = title.get_text(strip=True)
            
            metadata = full_body.find('div', class_="source")
            if metadata:
                meta_text = metadata.get_text(strip=True)
                if meta_text:
                    parts = meta_text.split('责编：')
                    if len(parts) == 2:
                        final_response['data']['meta_data']["Date"] = parts[0]
                        final_response['data']['meta_data']["Author"] = parts[1]
            
            body = full_body.find("div", class_="articleMain")
            if body:
                text = body.get_text(separator='\n', strip=True)
                lines = [line for line in text.split('\n') if line.strip()]
                if lines:
                    final_response['data']['body']["Text"] = lines
                else:
                    final_response['data']['body']["Text"] = [""]                    
            else:
                final_response['data']['body']["Text"] = ["Body content not found"]
        else:
            final_response["Message"] = "Article body not found"
        
        return final_response
    except requests.TooManyRedirects:
        final_response["Message"] = f"Too many redirects. Redirect history: {', '.join(response.history)}"
        final_response["Response"] = 310
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








