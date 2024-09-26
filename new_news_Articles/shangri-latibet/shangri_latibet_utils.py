import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin



def extract_shangri_latibet_page_article_links(url,):
    """
    Extracts all article links from a given shangri_latibet webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the shangri_latibet webpage containing article links.

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
        all_link_article = soup.find("ul", id="articleList")
        if all_link_article:
            article_block = all_link_article.find_all("a")
            if article_block:
                for each_link in article_block:
                    article_links = each_link.get("href")
                    if article_links:
                        all_links.append(article_links)
                        
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
import re
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime, timedelta

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

def scrape_shangri_latibet_article_content(url, tags):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.shangri-latibet.cn',
        'Referer': 'http://www.shangri-latibet.cn/node_5112_2.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }
    
    # Add If-Modified-Since header
    headers['If-Modified-Since'] = (datetime.utcnow() + timedelta(days=18)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Add If-None-Match header
    headers['If-None-Match'] = '"66dc7e9b-58da"'
    
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
        # Add a random delay before making the request
        time.sleep(random.uniform(1, 3))
        
        # Make the request to the URL using the retry session
        session = requests_retry_session()
        response = session.get(url, headers=headers, allow_redirects=False)
        response.raise_for_status()
        
        # Check for redirect
        if response.is_redirect:
            final_response["Message"] = f"Redirected to: {response.headers['Location']}"
            final_response["Response"] = response.status_code
            return final_response
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        tags_body = soup.find("ul", class_="breadcrumb")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('div', class_="page")
        if full_body:
            # Extract title
            title = full_body.find('h1')
            if title:
                title_text = title.get_text(strip=True)
            else:
                title_text = ""
            final_response['data']["title"] = title_text
            
            metadata = full_body.find('p', class_="sx")
            # Extracting Meta Data
            try:
                if metadata:
                    all_text = metadata.get_text(strip=True)
                    if all_text:
                        text = all_text
                        date_pattern = r'དུས་ཚོད།\s*(\d{4}-\d{2}-\d{2})'
                        author_source_pattern = r'(རྩོམ་པ་པོ།|རྩོམ་ཁུངས།)\s*(.+?)\s*(?:དུས་ཚོད།|རྩོམ་པ་པོ།|རྩོམ་ཁུངས།|$)'
                        # Extract date
                        date_match = re.search(date_pattern, text)
                        date = date_match.group(1) if date_match else ""
                        # Extract author and source
                        author_source = []
                        for match in re.finditer(author_source_pattern, text):
                            label = match.group(1)
                            content = match.group(2).strip()
                            author_source.append(f"{label} {content}")
                    
                        # Combine author and source
                        author_source_combined = " ".join(author_source)
                        final_response['data']['meta_data']["Date"] = date
                        final_response['data']['meta_data']["Author"] = author_source_combined
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
        # Extract body content
        try:
            body = full_body.find("div")
            if body:
                paragraphs = body.find_all("p")
                if paragraphs:
                    final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]
                else:
                    final_response['data']['body']["Text"] = [""]
        except AttributeError as e:
            final_response['data']['body']["Text"] = [f"Error fetching body content: {str(e)}"]
        
        return final_response
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408  # Request Timeout
        return final_response
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the article: {str(e)}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response










