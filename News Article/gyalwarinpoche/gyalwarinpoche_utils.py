import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import time



def extract_all_gyalwarinpoche_article_links(url: str) -> Dict[str, Any]:
    """
    Extracts all article links from a given gyalwarinpoche webpage.

    Args:
    url (str): The URL of the gyalwarinpoche webpage containing article links.

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
    load_more = False
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=(5, 60-5))
        response.raise_for_status()
        end_time = time.time()
        if end_time - start_time > 50:
            print(f"This URL took more than 50s: {url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        article_div = soup.find("div", class_="grid grid-thirds")
        if not article_div:
            raise ValueError("Could not find the main article container on the page.")
        
        all_articles = article_div.find_all("div", class_="cardImage")
        if not all_articles:
            raise ValueError("Could not find the each article container on the page.")
        article_links = []
        for article in all_articles:
            links = article.find("a")
            if links.get("href"):
                article_links.append(links.get("href"))
        
        final_response["Links"] = article_links

        load_more_span = soup.find("section", role="loadMore")
        if load_more_span:
            load_more = True

        return final_response, load_more
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
        return final_response, True
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response, True
    except ValueError as e:
        final_response["Message"] = f"An error occurred while parsing the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response, True
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response, True






def scrape_gyalwarinpoche_article_content(url):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "No Audio in GyalwaRinpoche", "Text": []},
            'meta_data': {'URL': url, 'Author': "", 'Date': "", 'Tags': []}
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
        
        # getting title, date, tags
        # section role="header"
        Tag_title_date = soup.find("section", role="header")
        
        # Extract title
        title_h1 = Tag_title_date.find("h1")
        if title_h1:
            title_text = title_h1.contents[0].strip()
            date_time = title_h1.span.text.strip()
            # title_text = title_h1.get_text(strip=True) if title_h1 else "Title not found"
        else:
            title_text = "Title not found"
            date_time = None
        final_response['data']["title"] = title_text
        final_response['data']['meta_data']["Date"] = date_time
        # for tags
        tag_list = []
        All_Tags = Tag_title_date.find('div', class_="controls")
        if All_Tags:
            tag_list.append(All_Tags.get_text(strip=True))          
        final_response['data']['meta_data']["Tags"] = tag_list
        
        # Extract body content
        try:
            body = soup.find('section', role='newsPost')
            if body:
                # print(body)
                # Extracting all <p> tags for text content
                paragraphs = body.find_all('p')
                final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]
            else:
                final_response['data']['body']["Text"] = ["No Content in the article"]

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
        final_response["Message"] = f"An error occurred in code: {str(e)}"
        final_response["Response"] = 404
        return final_response







