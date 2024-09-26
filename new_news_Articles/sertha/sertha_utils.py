import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin



def extract_sertha_page_article_links(url,):
    """
    Extracts all article links from a given sertha webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the sertha webpage containing article links.

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
        all_link_article = soup.find("div", class_="elementor-column elementor-col-50 elementor-top-column elementor-element elementor-element-c800525")
        if all_link_article:
            article_block = all_link_article.find_all("h3", class_="elementor-post__title")
            if article_block:
                for each_head in article_block:
                    article_links = each_head.find("a")
                    if article_links:
                        full_url = article_links.get("href")
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


def scrape_sertha_article_content(url, tags):
    headers = {
        # ':authority': 'sertha.net',
        # ':method': 'GET',
        # ':path': '/2022/12/04/%e0%bd%a6%e0%be%b2%e0%bd%b2%e0%bd%91%e0%bc%8b%e0%bd%94%e0%bd%a0%e0%bd%b2%e0%bc%8b%e0%bd%82%e0%be%b2%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%81%e0%be%b1%e0%bd%ba%e0%bd%a2%e0%bc%8b%e0%bd%93%e0%bd%a6%e0%bc%8b/',
        # ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://sertha.net/category/hhdl/%e0%bd%98%e0%bd%9b%e0%bd%91%e0%bc%8b%e0%bd%a2%e0%be%a3%e0%bd%98%e0%bc%8d-%e0%be%8b%e0%bd%82%e0%bd%bc%e0%bd%84%e0%bc%8b%e0%bd%a6%e0%bc%8b%e0%bd%98%e0%bd%86%e0%bd%bc%e0%bd%82/',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
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
        tags_body = soup.find("span", class_="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-terms")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('section', class_="elementor-section elementor-top-section elementor-element elementor-element-f29ac48 elementor-section-boxed elementor-section-height-default elementor-section-height-default")
        if full_body:
            # Extract title
            title = full_body.find('h1', class_="elementor-heading-title elementor-size-large")
            if title:
                title_text = title.get_text(strip=True)
                final_response['data']["title"] = title_text
            
            metadata = full_body.find('ul', class_="elementor-inline-items elementor-icon-list-items elementor-post-info")
            # Extracting Meta Data
            try:
                if metadata:
                    date_box = metadata.find("span", class_="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date")
                    if date_box:
                        final_response['data']['meta_data']["Date"] = date_box.get_text(strip=True)

                    author_box = metadata.find("span", class_="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-author")
                    if author_box:
                        final_response['data']['meta_data']["Author"] = author_box.get_text(strip=True)
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
            # Extract body content
            try:
                body = full_body.find("div", class_="elementor-element elementor-element-3979e3e elementor-widget elementor-widget-theme-post-content")
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












