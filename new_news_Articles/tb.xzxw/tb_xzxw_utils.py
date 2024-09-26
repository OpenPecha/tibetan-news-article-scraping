import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin




def extract_tb_xzxw_page_article_links(url,):
    """
    Extracts all article links from a given tb_xzxw webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the tb_xzxw webpage containing article links.

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
        all_link_article = soup.find("div", class_="sj_left_list")
        if all_link_article:
            article_block = all_link_article.find_all("div", class_="sj_left_list_title")
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



def scrape_tb_xzxw_article_content(url, tags):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221921d97a9f3ed0-0af301c17e118f-4c657b58-1188554-1921d97a9f4bab%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyMWQ5N2E5ZjNlZDAtMGFmMzAxYzE3ZTExOGYtNGM2NTdiNTgtMTE4ODU1NC0xOTIxZDk3YTlmNGJhYiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221921d97a9f3ed0-0af301c17e118f-4c657b58-1188554-1921d97a9f4bab%22%7D',
        'Host': 'tb.xzxw.com',
        'Referer': 'https://tb.xzxw.com/wxys/node_25972.html',
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
        tags_body = soup.find("div", class_="sj4_left_nav")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('div', class_="sj4_left_list")
        if full_body:
            # Extract title
            title = full_body.find('p', class_="second_title")
            if title:
                title_text = title.get_text(strip=True)
            else:
                title = full_body.find('p', class_="first_title")
                if title:
                    title_text = title.get_text(strip=True)
                else:
                    title = full_body.find('p', class_="third_title")
                    if title:
                        title_text = title.get_text(strip=True)
                    else:
                        title_text = ""
            final_response['data']["title"] = title_text
            
            metadata = full_body.find('span', class_="item_content")
            # Extracting Meta Data
            try:
                if metadata:
                    all_text = metadata.get_text(strip=True)
                    if all_text:
                        text = all_text                
                        # Extract date
                        date_pattern = r'སྤེལ་དུས།\s*(\d{4}-\d{2}-\d{2})'
                        date_match = re.search(date_pattern, text)
                        if date_match:
                            final_response['data']['meta_data']["Date"] = date_match.group(1)
                            
                        # Extract source
                        source_pattern = r'ཡོང་ཁུངས།\s*(.+?)\s*(?:\||$)'
                        source_match = re.search(source_pattern, text)
                        Source = ""
                        if source_match:
                            Source = source_match.group(1).strip()
                
                        # Extract author
                        author_pattern = r'རྩོམ་པ་པོ།\s*(.+?)\s*(?:\||$)'
                        author_match = re.search(author_pattern, text)
                        Author = ""
                        if author_match:
                            Author = author_match.group(1).strip()
                        full_Author_source = Author + " ཡོང་ཁུངས།: " + Source
                        final_response['data']['meta_data']["Author"] = full_Author_source
                        
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
        # Extract body content
        try:
            body = full_body.find("div", class_="sj4_left_list_abstract")
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














