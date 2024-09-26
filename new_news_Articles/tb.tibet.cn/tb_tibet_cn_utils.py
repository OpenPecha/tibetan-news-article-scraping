import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin


def extract_all_tb_tibet_cn_page_article_links(url, base_url):
    """
    Extracts all article links from a given tb_tibet_cn webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the tb_tibet_cn webpage containing article links.

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

        # Extracting all the articles in the DIV
        article_block = soup.find("div", class_="block_L fl")
        if article_block: 
            all_article = article_block.find_all("a", target="_blank")
            if all_article:
                for each_head in all_article:
                    # article_links = each_head.find("a")
                    if each_head is not None:
                        # Construct the full URL
                        full_url = urljoin(base_url, each_head.get("href"))
                        all_links.append(full_url)

        # if len(all_links) < 4:
        #     all_article = soup.find_all("div", class_="w-post-elm post_image usg_post_image_1 has_ratio with_placeholder")
        #     if all_article:
        #         for each_head in all_article:
        #             article_links = each_head.find("a")
        #             if article_links is not None:
        #                 all_links.append(article_links.get("href"))


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






def scrape_tb_tibet__article_content(url, tags):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
        # Make the request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        full_body = soup.find('div', id="contentK")
        # print(full_body)
        if full_body:
            # Extract title
            title = soup.find('h1')
            if title:
                title_text = title.get_text(strip=True)
            else:
                title_text = "no"
            final_response['data']["title"] = title_text
            
            metadata = soup.select('div.xinxi span')
            # Extracting Meta Data
            try:
                if len(metadata):
                    # Extract date
                    date = metadata[0].text.split()[-1]
                    # Extract author
                    author = metadata[1].text.split('། ', 1)[-1]
                    
                    final_response['data']['meta_data']["Date"] = date
                    final_response['data']['meta_data']["Author"] = author
               
            except AttributeError:
                final_response['data']['meta_data']["Author"] = "Error fetching author"
                final_response['data']['meta_data']["Date"] = "Error fetching date"
            
        # Extract body content
        try:
            body = full_body.find("div", class_="TRS_Editor")
            if body:
                paragraphs = body.find_all("font")
                if paragraphs:
                    # Extracting all <p> tags for text content
                    final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]
                else:
                    final_response['data']['body']["Text"] = [""]

        except AttributeError as e:
            final_response['data']['body']["Text"] = [f"Error fetching body content{str(e)}"]
        
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
        # print(f"An unexpected error occurred: {e}")
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response










