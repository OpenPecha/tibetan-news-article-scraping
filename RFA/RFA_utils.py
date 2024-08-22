import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import time

def extract_all_RFA_article_links(url: str) -> Dict[str, Any]:
    """
    Extracts all article links from a given RFA (Radio Free Asia) webpage.

    Args:
    url (str): The URL of the RFA webpage containing article links.

    Returns:
    Dict[str, Any]: A dictionary containing article links and status details.
    """
    headers = {
        "authority": "www.rfa.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "cache-control": "max-age=0",
        "cookie": "AMCVS_518ABC7455E462B97F000101%40AdobeOrg=1; s_cc=true; s_sq=%5B%5BB%5D%5D; utag_main=v_id:019169eade56002296e6ea4a443c0507d001b075008f7$_sn:2$_se:6$_ss:0$_st:1724132420582$vapi_domain:rfa.org$ses_id:1724127626756%3Bexp-session$_pn:6%3Bexp-session; AMCV_518ABC7455E462B97F000101%40AdobeOrg=1176715910%7CMCIDTS%7C19955%7CMCMID%7C92058839809215745258174654077801968713%7CMCAID%7CNONE%7CMCOPTOUT-1724137821s%7CNONE%7CvVersion%7C5.4.0",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
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
        all_articles = soup.find_all("div", class_="teaserimg")
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



def scrape_rfa_article(url: str, tags="གསར་འགྱུར།") -> Dict[str, Any]:
    """
    Scrapes an article from the RFA (Radio Free Asia) website.

    Args:
    url (str): The URL of the RFA article to scrape.

    Returns:
    Dict[str, Any]: A dictionary containing the scraped information and status details.
    """
    headers = {
        "authority": "www.rfa.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "cache-control": "max-age=0",
        "cookie": "AMCVS_518ABC7455E462B97F000101%40AdobeOrg=1; s_cc=true; s_sq=%5B%5BB%5D%5D; utag_main=v_id:019169eade56002296e6ea4a443c0507d001b075008f7$_sn:2$_se:6$_ss:0$_st:1724132420582$vapi_domain:rfa.org$ses_id:1724127626756%3Bexp-session$_pn:6%3Bexp-session; AMCV_518ABC7455E462B97F000101%40AdobeOrg=1176715910%7CMCIDTS%7C19955%7CMCMID%7C92058839809215745258174654077801968713%7CMCAID%7CNONE%7CMCOPTOUT-1724137821s%7CNONE%7CvVersion%7C5.4.0",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    
    final_response = {
        "data": {
            'title': "",
            'body': {"Audio": "", "Text": []},
            'meta_data': {'URL': url, 'Author': "RFA.org", 'Date': "", 'Tags': [tags]}
        },
        "Message": "Success",
        "Response": 200
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=120)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)
        # Extract title
        title_data_data = soup.find('div', class_='mobilecontainer')
        title = title_data_data.find("h1")
        final_response['data']['title'] = title.text.strip() if title else "Title not found"

        data_data = title_data_data.find("div", id="dateline")
        final_response['data']['meta_data']["Date"] = data_data.text.strip() if data_data else ""

        # Extract body content ### dont use class_="gmail_quote"
        body = soup.find('div', id='storytext')
        if body:
            paragraphs = body.find_all('p')
            final_response['data']['body']["Text"] = [para.get_text(strip=True) for para in paragraphs]

        # Find the audio tag and get its src attribute
        audio = soup.find('audio', class_="story_audio")
        if audio:
            final_response['data']['body']["Audio"] = audio.get('src', "No audio source found")
        else:
            final_response['data']['body']["Audio"] = "No audio source found"

        return final_response
    
    except requests.Timeout:
        final_response["Message"] = "Request timed out"
        final_response["Response"] = 408
        return final_response
        
    except requests.RequestException as e:
        final_response["Message"] = f"An error occurred while fetching the article: {e}"
        final_response["Response"] = getattr(e.response, 'status_code', 500)
        return final_response
