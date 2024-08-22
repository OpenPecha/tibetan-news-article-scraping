import requests
from bs4 import BeautifulSoup
import json
import time






def extract_all_tt_page_article_links(url: str):
    """
    Extracts all article links from a given TibetTimes webpage.

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
        
        # Extracting all the articles in the DIV
        all_article = soup.find_all("h3", class_="jeg_post_title")
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







def scrape_tt_article_content(url, tags="གསར་འགྱུར།"):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "No Audio in TibetTimes", "Text": []},
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
        
        # Extract title
        title = soup.find('div', class_="entry-header")
        if title:
            title_h1 = title.find("h1", class_="jeg_post_title")
            title_text = title_h1.get_text(strip=True) if title_h1 else "Title not found"
        else:
            title_text = "Title not found"
        final_response['data']["title"] = title_text

        
        # Extracting Meta Data
        try:
            meta_data_body = soup.find('div', class_="jeg_post_meta jeg_post_meta_1")
            if meta_data_body:
                author_name = meta_data_body.find('div', class_="jeg_meta_author")
                final_response['data']['meta_data']["Author"] = author_name.get_text(strip=True) if author_name else "Author not found"
                
                date_time = meta_data_body.find('div', class_="jeg_meta_date")
                final_response['data']['meta_data']["Date"] = date_time.get_text(strip=True) if date_time else "Date not found"
        except AttributeError:
            final_response['data']['meta_data']["Author"] = "Error fetching author"
            final_response['data']['meta_data']["Date"] = "Error fetching date"


        # Extract body content
        try:
            body = soup.find('div', class_='entry-content with-share')
            if body:
                # print(body)
                inner_content = body.find("div", class_="content-inner")
                if inner_content:
                    # Extracting all <p> tags for text content
                    paragraphs = inner_content.find_all('p')
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



