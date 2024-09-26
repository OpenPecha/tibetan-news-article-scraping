import requests
from bs4 import BeautifulSoup
import json
import time
import re



def extract_all_khabdha_page_article_links(url: str):
    """
    Extracts all article links from a given khabdha webpage.

    This function scrapes the provided URL and extracts links to individual articles
    found on the page.

    Args:
    url (str): The URL of the khabdha webpage containing article links.

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
        all_article = soup.find_all("h2", class_="entry-title")
        if all_article:
            for each_head in all_article:
                article_links = each_head.find("a")
                if article_links is not None:
                    all_links.append(article_links.get("href"))

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






def scrape_khabdha_article_content(url,):
    """
    
    
    """


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "", "Text": []},
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
        
        # Extract title
        title = soup.find('h1', class_="entry-title")
        if title:
            title_text = title.get_text(strip=True) 
        else:
            title_text = ""
        final_response['data']["title"] = title_text

        
        # Extracting Meta Data
        try:
            date_time = soup.find("time", class_="entry-date published")
            final_response['data']['meta_data']["Date"] = date_time.get_text(strip=True) if date_time else "No date"
            
            if date_time == None: 
                date_time = soup.find("time", class_="entry-date published updated")
                final_response['data']['meta_data']["Date"] = date_time.get_text(strip=True) if date_time else "No date"


            author_name = soup.find('span', class_="posted-by byline")
            full_text = author_name.find('a').text.strip() if author_name else ""
            # Use regex to extract only the Tibetan text
            final_response['data']['meta_data']["Author"] = re.search(r'[\u0F00-\u0FFF]+', full_text).group()
        except AttributeError:
            final_response['data']['meta_data']["Author"] = "Error fetching author"
            final_response['data']['meta_data']["Date"] = "Error fetching date"

        category = soup.find("span", class_="cat-links")
        category_tags = category.find_all('a', rel="category tag")
        # Extract and print the category names
        final_response['data']['meta_data']["Tags"] = [tag.text for tag in category_tags]

        # Extract body content
        try:
            body = soup.find('div', class_='pb-content')
            if body:
                paragraphs = body.find_all('p')
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









