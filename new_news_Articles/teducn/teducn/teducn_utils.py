import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin



def extract_teducn_page_article_links(url,):
    """
    Extracts all article links from a given teducn webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the teducn webpage containing article links.

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
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'cache-control': 'max-age=0',
        'connection': 'keep-alive',
        'cookie': 'rhldeecookieinforecord=%2C168-99%2C',
        'host': 'www.teducn.com',
        'if-modified-since': '{modified_since}',
        'if-none-match': '{etag}',
        'referer': '{referer}',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
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
        article_block = soup.find("td", class_="down_list")
        if article_block:
            for each_head in article_block:
                article_links = each_head.find_all("a")
                if article_links:
                    for each_link in article_links:
                        full_url = each_link.get("href")
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


def scrape_teducn_article_content(url, tags):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'cache-control': 'max-age=0',
        'connection': 'keep-alive',
        'cookie': 'rhldeecookieinforecord=%2C168-99%2C',
        'host': 'www.teducn.com',
        'if-modified-since': '{modified_since}',
        'if-none-match': '{etag}',
        'referer': '{referer}',
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

        # Find the specific table
        tags_table = soup.find('table', attrs={
            'width': '100%',
            'border': '0',
            'cellpadding': '2',
            'cellspacing': '1',
            'bgcolor': '#DBF3FF'
            })
        print(tags_table)
        if tags_table:
            links = tags_table.find_all('a')
            # Extract href and text from each link
            extracted_links = [link.get_text(strip=True) for link in links]
            print(extracted_links)
            final_response['data']['meta_data']["Tags"] = extracted_links 

        # Find the specific table
        table = soup.find('table', class_='title_info')
        print(table)
        if table:
        
            # Extract title
            title_span = table.find('span', class_='lan_19')
            title = title_span.get_text(strip=True) if title_span else None
            
            # Extract date and author/source
            info_td = table.find('td', class_='hei_zw')
            if info_td:
                info_text = info_td.get_text(strip=True)
                
                # Extract date
                date_match = re.search(r'སྤེལ་དུས།(\d{2}-\d{2})', info_text)
                date = date_match.group(1) if date_match else None
                
                # Extract author and source
                author_source = re.sub(r'སྤེལ་དུས།\d{2}-\d{2}', '', info_text).strip()
                author_source = re.sub(r'ཡོང་ཁུངས།|རྩོམ་པ་པོ།', '', author_source).strip()
            else:
                date = None
                author_source = None

            final_response['data']["title"] = title
            final_response['data']['meta_data']["Author"] = author_source
            final_response['data']['meta_data']["Date"] = date
            
       # Extract body content
        try:
            body = soup.find("span", class_="txt")
            if body:
                # Extract all text content, including spans
                all_text = body.find_all(string=True)
                
                # Filter out empty strings and strip whitespace
                filtered_text = [text.strip() for text in all_text if text.strip()]
                
                # Remove duplicate consecutive lines (which often occur due to formatting)
                final_text = []
                for line in filtered_text:
                    if not final_text or line != final_text[-1]:
                        final_text.append(line)
                
                final_response['data']['body']["Text"] = final_text
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






