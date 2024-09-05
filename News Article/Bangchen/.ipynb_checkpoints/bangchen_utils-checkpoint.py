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




def scrape_Bangchen_article_content(url):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "No Audio in Bangchen", "Text": []},
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
        
        Tag_title_date = soup.find("div", class_="entry-header-details")
        if Tag_title_date is None:
            raise requests.RequestException("No title found: check class=entry-header-details")
        
        # Extract title
        title_h1 = Tag_title_date.find("h1", class_="entry-title")
        if title_h1:
            title_text = title_h1.get_text(strip=True) if title_h1 else "Title not found"
        else:
            title_text = "Title not found"
        final_response['data']["title"] = title_text

        # for tags
        tag_list = []
        All_Tags = Tag_title_date.find_all('a', class_="covernews-categories category-color-1")
        for each_tag in All_Tags:
            if each_tag.get_text():
                tag_list.append(each_tag.get_text(strip=True))
        final_response['data']['meta_data']["Tags"] = tag_list
        
        # Extracting Meta Data
        try:
            meta_data_body = Tag_title_date.find('span', class_="author-links")
            if meta_data_body:
                author_name = meta_data_body.find('span', class_="item-metadata posts-author")
                final_response['data']['meta_data']["Author"] = author_name.get_text(strip=True) if author_name else "Author not found"
                
                date_time = meta_data_body.find('span', class_="item-metadata posts-date")
                final_response['data']['meta_data']["Date"] = date_time.get_text(strip=True) if date_time else "Date not found"
        except AttributeError:
            final_response['data']['meta_data']["Author"] = "Error fetching author"
            final_response['data']['meta_data']["Date"] = "Error fetching date"


        # Extract body content
        try:
            body = soup.find('div', class_='entry-content')
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







