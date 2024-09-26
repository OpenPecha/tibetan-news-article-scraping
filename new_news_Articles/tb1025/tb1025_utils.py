import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry




def extract_tb1025_page_article_links(url, base_url):
    """
    Extracts all article links from a given tb1025 webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the tb1025 webpage containing article links.

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
        all_link_article = soup.find("ul", class_="list-group")
        if all_link_article:
            article_block = all_link_article.find_all("a", target="_blank")
            if article_block:
                for each_link in article_block:
                    article_links = each_link.get("href")
                    if article_links:
                        full_url = urljoin(base_url, article_links)
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



def scrape_tb1025_article_content(url, tags):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.tb1025.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
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
        response = session.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        tags_body = soup.find("ol", class_="breadcrumb")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('div', class_="main-box")
        if full_body:
            # Extract title
            title = soup.find('h4')
            if title:
                title_text = title.get_text(strip=True)
            else:
                title_text = ""
            final_response['data']["title"] = title_text
            
            metadata = full_body.find('div', class_="info")
            # Extracting Meta Data
            try:
                if metadata:
                    all_text = metadata.get_text(strip=True)
                    if all_text:
                        text = re.sub(' +', ' ', all_text)
                        date_pattern = r'སྤེལ་དུས།\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
                        author_pattern = r'རྩོམ་པ་པོ།\s*(.+?)\s*(?:ཀློག་ཐེངས།|$)'
                        date_match = re.search(date_pattern, text)
                        date = date_match.group(1) if date_match else ""
                        author_match = re.search(author_pattern, text)
                        author = author_match.group(1).strip() if author_match else ""
                        final_response['data']['meta_data']["Date"] = date
                        final_response['data']['meta_data']["Author"] = author
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
        # Extract body content
        try:
            body = full_body.find("div", class_="main")
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










