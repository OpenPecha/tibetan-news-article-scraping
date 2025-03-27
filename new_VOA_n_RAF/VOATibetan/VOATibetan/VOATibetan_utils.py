import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Tuple, Optional
import time



def check_media(html_parse) -> Optional[str]:
    """
    Check if the HTML element contains video content and extract article URL if not.
    
    Args:
        html_parse: BeautifulSoup parsed HTML element
        
    Returns:
        Optional[str]: Full URL to the article or None if it's a video or no link found
    """
    # Check if it's a video content
    media_type = html_parse.find("span", class_="ico-video")
    if media_type:
        return None
    
    # Find the link - using find instead of direct attribute access for safety
    links = html_parse.find("a")
    if links and links.get("href"):
        url = "https://www.voatibetan.com" + links.get("href")
        return url
    
    return None  # Return None if no valid link found


def convert_tibetan_date(tibetan_date: str) -> Tuple[int, int, int]:
    """
    Convert a Tibetan date string to year, month, day integers.
    
    Args:
        tibetan_date (str): Tibetan date string
        
    Returns:
        Tuple[int, int, int]: (year, month, day)
        
    Raises:
        ValueError: If date cannot be parsed properly
    """
    # Dictionary for Tibetan month names
    tibetan_months = {
        "དང་པོ": 1, "གཉིས་པ": 2, "གསུམ་པ": 3, "བཞི་པ": 4, "ལྔ་པ": 5, 
        "དྲུག་པ": 6, "བདུན་པ": 7, "བརྒྱད་པ": 8, "དགུ་པ": 9, "བཅུ་པ": 10,
        "བཅུ་གཅིག་པ": 11, "བཅུ་གཉིས་པ": 12
    }
    
    # Dictionary for Tibetan numerals
    tibetan_numerals = {
        "༠": "0", "༡": "1", "༢": "2", "༣": "3", "༤": "4",
        "༥": "5", "༦": "6", "༧": "7", "༨": "8", "༩": "9"
    }
    
    try:
        # Split the date components
        parts = tibetan_date.split("།")
        if len(parts) < 3:
            raise ValueError(f"Invalid date format: {tibetan_date}")
        
        # Extract month
        month_part = parts[0]
        month = None
        for month_name, month_num in tibetan_months.items():
            if month_name in month_part:
                month = month_num
                break
        
        # If month not found through dictionary lookup, try to handle specific cases
        if month is None:
            # Check for specific month patterns
            for i, (month_name, month_num) in enumerate(tibetan_months.items()):
                if month_name in month_part:
                    month = month_num
                    break
            
            # If still not found, try numeric patterns
            if month is None:
                for i in range(1, 13):
                    month_patterns = [
                        f"ཟླ་{i}", 
                        f"སྤྱི་ཟླ་{i}",
                        f"ཟླ་{tibetan_months.get(i, '')}"
                    ]
                    if any(pattern in month_part for pattern in month_patterns):
                        month = i
                        break
        
        # If still no month identified, raise error
        if month is None:
            raise ValueError(f"Could not identify month in: {month_part}")
        
        # Extract day
        day_text = parts[1].strip()
        day = ""
        for char in day_text:
            if char in tibetan_numerals:
                day += tibetan_numerals[char]
        
        if not day:
            raise ValueError(f"Could not extract day from: {day_text}")
        
        day = int(day)
        
        # Extract year
        year_text = parts[2].strip()
        year = ""
        for char in year_text:
            if char in tibetan_numerals:
                year += tibetan_numerals[char]
        
        if not year:
            raise ValueError(f"Could not extract year from: {year_text}")
        
        year = int(year)
        
        # Basic validation
        if not (1 <= month <= 12 and 1 <= day <= 31 and 1900 <= year <= 2100):
            raise ValueError(f"Date values out of reasonable range: {year}-{month}-{day}")
            
        return year, month, day
    
    except Exception as e:
        raise ValueError(f"Error parsing Tibetan date '{tibetan_date}': {str(e)}")


def extract_all_VOATibetan_article_links(url: str, 
                                         connect_timeout: int = 5,
                                         read_timeout: int = 55) -> Tuple[Dict[str, Any], bool, List[int]]:
    """
    Extracts all article links from a given VOATibetan webpage.

    Args:
        url (str): The URL of the VOATibetan webpage containing article links.
        connect_timeout (int): Timeout for connection in seconds
        read_timeout (int): Timeout for reading response in seconds

    Returns:
        Tuple[Dict[str, Any], bool, List[int]]: 
            - A dictionary containing article links and status details
            - Boolean indicating if there are more pages to load
            - List containing [year, month, day] of the last article if found
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
    last_date = []
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=(connect_timeout, read_timeout))
        response.raise_for_status()
        end_time = time.time()
        
        if end_time - start_time > 50:
            print(f"This URL took more than 50s: {url}")
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main container
        article_div = soup.find("div", class_="col-xs-12 col-md-8 col-lg-8 pull-left content-offset")
        if not article_div:
            raise ValueError("Could not find the main article container on the page.")
            
        # Process first article
        first_link = article_div.find("div", class_="media-block")
        article_links = []
        
        if first_link:
            link1 = check_media(first_link)
            if link1:  # Only append if not None
                article_links.append(link1)
        
        # Process the rest of the articles
        all_articles_div = article_div.find("ul", id="ordinaryItems")
        if not all_articles_div:
            raise ValueError("Could not find the article container with ID 'ordinaryItems' on the page.")
        
        all_articles = all_articles_div.find_all("div", class_="media-block")
        last_article = None
        
        for article in all_articles:
            link = check_media(article)
            if link:  # Only append if not None
                article_links.append(link)
            last_article = article  # Keep track of the last article for date extraction
        
        # Store valid links in response
        final_response["Links"] = article_links

        # Check if there's a "load more" button
        load_more_span = soup.find("p", class_="buttons btn--load-more")
        load_more = bool(load_more_span)
        
        # If no more pages, try to get date from last article
        if not load_more and last_article:
            get_last_date_span = last_article.find("span", class_="date date--mb date--size-3")
            if get_last_date_span:
                date_text_tib = get_last_date_span.text.strip()
                try:
                    year, month, day = convert_tibetan_date(date_text_tib)
                    print(f"Last article date: {year}-{month}-{day}")
                    last_date = [year, month, day]
                except ValueError as e:
                    print(f"Error converting date: {e}")
                    last_date = []

        return final_response, load_more, last_date
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
        return final_response, False, []  # Changed to False since we couldn't determine
    
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the webpage: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500) if hasattr(e, 'response') else 500
        return final_response, False, []  # Changed to False since we couldn't determine
    
    except ValueError as e:
        final_response["Message"] = f"An error occurred while parsing the webpage: {e}"
        final_response["Response"] = 500  # ValueError doesn't have a response attribute
        return final_response, False, []  # Changed to False since we couldn't determine
    
    except Exception as e:
        final_response["Message"] = f"An unexpected error occurred: {e}"
        final_response["Response"] = 500
        return final_response, False, []  # Changed to False since we couldn't determine





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
        if title_data:
            final_response['data']["title"] = title_data.get_text(strip=True)  
        else:
            title_data = soup.find("div", class_="col-title col-xs-12 col-lg-10 pull-right")
            if title_data:
                final_response['data']["title"] = title_data.get_text(strip=True)  
            else:
                final_response['data']["title"] = ""
            

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

        ### due to mistake we can see that autor and date variable was switched
        final_response['data']['meta_data']["Author"] =  date_time
        final_response['data']['meta_data']["Date"] = author

        
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
                final_response['data']['body']["Text"] = []
        except AttributeError as e:
            final_response['data']['body']["Text"] = []


        if final_response['data']['body']["Text"] == []:
            # print("Empty")
            content_div = soup.find('div', class_='intro m-t-md')
            if content_div:
                # Extract all text content, 
                main_content = []
                # Get remaining text, excluding empty lines
                remaining_text = content_div.get_text(strip=True, separator='\n').split('\n')
                main_content.extend([text for text in remaining_text if text])
                
                final_response['data']['body']["Text"] = main_content
            else:
                final_response['data']['body']["Text"] = []
            

        
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

