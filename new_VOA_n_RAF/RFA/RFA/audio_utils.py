import requests
from bs4 import BeautifulSoup

def download_audio_from_rfa(url, output_filename):
    headers = {
        'authority': 'www.rfa.org',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'utag_main=v_id:019169eade56002296e6ea4a443c0507d001b075008f7$_sn:10$_se:1$_ss:1$_st:1727671960241$vapi_domain:rfa.org$ses_id:1727670160241%3Bexp-session$_pn:1%3Bexp-session; AMCVS_518ABC7455E462B97F000101%40AdobeOrg=1; AMCV_518ABC7455E462B97F000101%40AdobeOrg=1176715910%7CMCIDTS%7C19997%7CMCMID%7C92058839809215745258174654077801968713%7CMCAID%7CNONE%7CMCOPTOUT-1727677360s%7CNONE%7CvVersion%7C5.4.0; s_cc=true',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    
    # Send a GET request to the page
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to access the page. Status code: {response.status_code}")
        return
    
    # For audio streams, we might not need to parse the HTML
    # We can directly save the content as it's likely the audio file itself
    with open(output_filename, 'wb') as file:
        file.write(response.content)
    # print(f"Audio file downloaded successfully: {output_filename}")
