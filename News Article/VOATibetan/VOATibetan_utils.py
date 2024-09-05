import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import time

def check_media(html_parse):
    """
    
    """
    media_type = html_parse.find("span", class_="ico--media-type")
    if media_type:
        return None
    
    links = html_parse.find("a")
    if links:
        url = "https://www.voatibetan.com" + links.get("href")
        return url

    


def extract_all_VOATibetan_article_links(url: str) -> Dict[str, Any]:
    """
    Extracts all article links from a given VOATibetan webpage.

    Args:
    url (str): The URL of the VOATibetan webpage containing article links.

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
        
        article_div = soup.find("div", class_="col-xs-12 col-md-8 col-lg-8 pull-left content-offset")
        if not article_div:
            raise ValueError("Could not find the main article container on the page.")
        first_link = article_div.find("div", class_="media-block")

        
        article_links = []
        link1 = check_media(first_link)
        article_links.append(link1)
        
        all_articles_div = article_div.find("ul", id="ordinaryItems")
        if not all_articles_div:
            raise ValueError("Could not find the each article container on the page.")
        
        all_articles = all_articles_div.find_all("div", class_="media-block")
        for article in all_articles:
            link = check_media(article)
            if link:
                article_links.append(link)

        final_response["Links"] = article_links

        load_more_span = soup.find("p", class_="buttons btn--load-more")
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





def scrape_VOATibetan_article_content(url, Tags=""):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "", "Text": []},
            'meta_data': {'URL': url, 'Author': "", 'Date': "", 'Tags': [Tags]}
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
        title_data = soup.find("div", class_="col-title col-xs-12 col-md-10 pull-right")        
        # Extract title
        final_response['data']["title"] = title_data.get_text(strip=True) if title_data else ""

        # publishing-details and date
        date_author = soup.find("div", class_="publishing-details")
        if date_author:
            author_div = date_author.find("span", class_="date")
            author = author_div.get_text(strip=True) if author_div else ""

            date_div = date_author.find("a", class_="links__item-link")
            date_time = date_div.get_text(strip=True) if date_div else ""
        else:
            author_div = ""
            date_time = None
        final_response['data']['meta_data']["Author"] = author
        final_response['data']['meta_data']["Date"] = date_time

        
        # Extract audio content
        try:
            # Find the main audio link  wsw__embed
            audio_div = soup.find_all('div', class_='c-mmp__player')
            if len(audio_div):
                audio_sources = []
                # print(audio_div)
                for audio_div in audio_div:
                    # Find the audio element within each div
                    audio = audio_div.find('audio')
                    if audio and audio.get("src"):
                        audio_sources.append(audio.get("src"))
                final_response['data']['body']["Audio"] = audio_sources
            else:
                final_response['data']['body']["Audio"] = ""
        except AttributeError as e:
            final_response['data']['body']["Audio"] = ""
        
        # Extract body content
        try:
            # Find the main content div
            content_div = soup.find('div', class_='wsw')
            if content_div:
                # excluding wsw__embed elements which has all audio
                for embed in content_div.find_all(class_='wsw__embed'):
                    embed.decompose()
                # Extract all text content, 
                main_content = []
                # Get remaining text, excluding empty lines
                remaining_text = content_div.get_text(strip=True, separator='\n').split('\n')
                main_content.extend([text for text in remaining_text if text])
                
                final_response['data']['body']["Text"] = main_content
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



