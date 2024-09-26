import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin




def extract_all_kangbatv_page_article_links(url, base_url):
    """
    Extracts all article links from a given kangbatv webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the kangbatv webpage containing article links.

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
        all_link_article = soup.find("ul", class_="col-activity-list col-buddhism-list col-article-list")
        if all_link_article:
            article_block = all_link_article.find_all("li")
            # print(article_block)
            if article_block:
                for each_head in article_block:
                    article_links = each_head.find("a")
                    if article_links:
                        full_url = urljoin(base_url, article_links.get("href"))
                        all_links.append(full_url)
        else:
            all_link_article = soup.find("ul", class_="col-movies-list after")
            if all_link_article:
                article_block = all_link_article.find_all("li")
                # print(article_block)
                if article_block:
                    for each_head in article_block:
                        article_links = each_head.find("a")
                        # print(article_links)
                        if article_links:
                            full_url = urljoin(base_url, article_links.get("href"))
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

def scrape_kangbatv_article_content(url, tags):
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'tb.kangbatv.com',
            'Referer': 'https://tb.kangbatv.com/xw/gjxw/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
    
    # Add If-Modified-Since header
    # headers['If-Modified-Since'] = (datetime.utcnow() + timedelta(days=18)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # # Add If-None-Match header
    # headers['If-None-Match'] = '"66dc7e9b-58da"'
    
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


        tags_body = soup.find("ol", class_="cell_6603_ clearfix breadcrumb pull-left")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('div', class_="col-player-box pull-left")
        # print(full_body)
        if full_body:
            # Extract title
            title = soup.find('h3', class_="col-text-title text-center article-title")
            if title:
                title_text = title.get_text(strip=True)
            else:
                title_text = ""
            final_response['data']["title"] = title_text
            
            metadata = full_body.find('div', class_="col-text-brief after")
            # Extracting Meta Data
            try:
                if len(metadata):
                    # Extract date
                    date = metadata.find('div', class_="col-text-time white-nowrap pull-right")
                    if date:
                        final_response['data']['meta_data']["Date"] = date.get_text(strip=True)
                        
                    # Extract author
                    author = metadata.find('div', class_="col-text-from white-nowrap pull-right")
                    if author:
                        final_response['data']['meta_data']["Author"] = author.get_text(strip=True)
                        
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
            # Extract body content
            try:
                body = full_body.find("div", class_="article-main col-text-cont")
                if body:
                    paragraphs = body.find_all("p")
                    if paragraphs:
                        # Extracting all <p> tags for text content
                        final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]
                    else:
                        final_response['data']['body']["Text"] = [""]
    
            except AttributeError as e:
                final_response['data']['body']["Text"] = [f"Error fetching body content{str(e)}"]

        else:
            full_body = soup.find('div', class_="cell_14327_ col-living-player")
            if full_body:
                # Extract title
                title = soup.find('h1', class_="article-title video-title")
                if title:
                    title_text = title.get_text(strip=True)
                else:
                    title_text = ""
                final_response['data']["title"] = title_text
                
                metadata_box = full_body.find('table', class_="infotab")
                if metadata_box:
                    metadata = metadata_box.find_all('td')
                    # print(metadata)
                    # Extracting Meta Data
                    try:
                        if len(metadata):
                            # Extract date
                            date = metadata[1]
                            if date:
                                final_response['data']['meta_data']["Date"] = date.get_text(strip=True)
                                
                            # Extract author
                            author = metadata[0]
                            if author:
                                final_response['data']['meta_data']["Author"] = author.get_text(strip=True)
                    except AttributeError:
                        final_response['data']['meta_data']["Author"] = "Error fetching author"
                        final_response['data']['meta_data']["Date"] = "Error fetching date"
        
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








