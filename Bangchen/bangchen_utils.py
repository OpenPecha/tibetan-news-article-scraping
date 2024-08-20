import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import time



def extract_all_Bangchen_article_links(url: str) -> Dict[str, Any]:
    """
    Extracts all article links from a given Bangchen webpage.

    Args:
    url (str): The URL of the Bangchen webpage containing article links.

    Returns:
    Dict[str, Any]: A dictionary containing article links and status details.
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
        if end_time - start_time > 50:
            print(f"This URL took more than 50s: {url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        article_div = soup.find("div", class_="content-area")
        all_articles = article_div.find_all("div", class_="post-thumbnail")
        if not all_articles:
            raise ValueError("Could not find the main article container on the page.")
        
        article_links = []
        for article in all_articles:
            links = article.find("a")
            if links.get("href"):
                article_links.append(links.get("href"))
        
        final_response["Links"] = article_links
        return final_response
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
        return final_response
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response
    except ValueError as e:
        final_response["Message"] = f"An error occurred while parsing the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response









