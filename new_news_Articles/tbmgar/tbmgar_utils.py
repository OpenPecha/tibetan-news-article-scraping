import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin




def extract_tbmgar_page_article_links(url, base_url):
    """
    Extracts all article links from a given tbmgar webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the tbmgar webpage containing article links.

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
        article_block = soup.find_all("div", id="lcqwJbzJW")
        if article_block:
            for each_head in article_block:
                article_links = each_head.find_all("a")
                if article_links:
                    for each_link in article_links:
                        full_url = urljoin(base_url, each_link.get("href"))
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


def scrape_tbmgar_article_content(url, tags):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'ASPSESSIONIDSQARQCCS=OPDBAEHAACOIGINHPMDBLDGF; ASPSESSIONIDAASRQDDR=CGLLDFIANLMPGNLNMCKEOJHN; ASPSESSIONIDCCRQSCBQ=IBMDFKJAEGAGHEDEJOENKNHL; sdwaf-test-item=a83326000653520907520256510356000f5d03530c520b000455025000030a07030f514c0753511702501c54515d1e0005',
        'Host': 'www.tbmgar.com',
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

        tags_body = soup.find("td", class_="xczdNzd")
        tags = []
        if tags_body:
            tag_list = tags_body.find_all("a")
            if tag_list:
                for tag in tag_list:
                    each_tag = tag.get_text(strip=True)
                    tags.append(each_tag)
                final_tag = tags_body.find("font")
                if final_tag:
                    tags.append(final_tag.get_text(strip=True))
                final_response['data']['meta_data']["Tags"] = tags
        
        full_body = soup.find('table', class_="ndbwTT")
        if full_body:
            # Extract title
            title = soup.find('font', class_='NdbwKx')
            if title:
                title_text = title.get_text(strip=True)
            else:
                title_text = ""
            final_response['data']["title"] = title_text
            
            metadata = full_body.find('table', class_="ND_zzbSYg")
            # Extracting Meta Data
            try:
                if metadata:
                    each_meta = metadata.find_all("td")
                    if each_meta:
                        # Extract author
                        author = each_meta[0].get_text(strip=True)
                        # Extract date
                        date_text = each_meta[1].get_text(strip=True)
                        date = re.search(r'\d{4}/\d{1,2}/\d{1,2}', date_text)
                        if date:
                            final_response['data']['meta_data']["Date"] = date.group()
                        final_response['data']['meta_data']["Author"] = author
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
       # Extract body content
        try:
            body = full_body.find("table", id="Nd_mni")
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





