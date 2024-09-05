import requests
from bs4 import BeautifulSoup
import json
import time


def extract_all_tt_page_article_links(url: str):
    """
    Extracts all article links from a given VOT (Voice of Tibet) webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the VOT webpage containing article links.

    Returns:
        {
            "Links": List[],
            "Message": string,
            "Response": int
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
        "Response": 200
    }
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=(5, 60-5))
        response.raise_for_status()
        end_time = time.time()

        if end_time-start_time > 50:
            print(f"This ULR Took more then 50s: {url}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting all the articles in the DIV
        all_article = soup.find_all("h3", class_="jeg_post_title")
        print(type(all_article))
        if not all_article:
            raise ValueError("Could not find the main article container on the page.")
        
        
        # # Getting all the links of articles 
        all_links = []
        for each_head in all_article:
            article_links = each_head.find("a")
            if article_links is not None:
                all_links.append(article_links.get("href"))
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








