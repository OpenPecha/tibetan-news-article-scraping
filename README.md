# Objective
Develop scripts to efficiently scrape Tibetan news articles from multiple sources, starting with the Voice of Tibet (VOT) website, and store them in a structured format for training a machine translation model.

## Description
We need Tibetan news articles for training our machine translation model. This task involves creating scripts to collect articles from various Tibetan news websites, beginning with VOT, and organizing them in a clear, structured format.

## Data link:
- https://drive.google.com/drive/folders/170EW3j3150nbcioQrUEG0hBoxW-RabIg?usp=sharing
- **Note:** Only view access is granted to **Esukhia and Monlam AI** employees with the appropriate email extension.


## Completion Criteria
- Scripts developed that can efficiently scrape **all the Tibetan news articles from VOT and other sources.**
- Collected articles stored in a structured format (JSON) suitable for use in machine translation training.
- Collect **audio and meta-data if available.**

## Tibetan News Websites to be Extracted
- https://vot.org/ (implemented)
    - Audio related to the article
- https://tibettimes.net/ (implemented)
    - No Audio
- https://www.voatibetan.com/ (implemented)
    - Audio not that related
- https://www.rfa.org/tibetan (implemented)
    - Audio Seems related
- http://bangchen.net/ (dead site)
- http://bangchen.tibetexpress.net  (implemented)
    - No Audio
- https://www.gyalwarinpoche.com/ (implemented)
    - No Audio
- https://bod.asia/ (implemented)

## Tibetan to English Translation Websites to be Extracted:
- https://linguatools.info/ (implemented)
- https://app.glosbe.com/ (implemented)

## Subtasks
1. Implement a function to collect All article links from Website
2. Implement a function to extract detailed information from individual articles links
3. Extend the existing code to handle other Tibetan news websites
4. Organize the collected news articles in a clear and structured format in **JSON** format


## Data Structure
The scraped article link for each page is stored in a dictionary with the following structure:
```python
{
    "Links": List[],
    "Message": string,
    "Response": int
}

```


The scraped data for each article is stored in a dictionary with the following structure:

```python
{
    "data": {
        "title": str,
        "body": {
            "Audio": str,
            "Text": List[str]
        },
        "meta_data": {
            "Author": str,
            "Date": str,
            "Tags": List[str],
            "URL": str
        }
    },
    "Message": str,
    "Response": int
}
```

Language Translation format:
```python
translation_format = {
        "data": {
            "English": {
                    'Word': "",
                    'POS': "",
                    'Sentence': ""
                },
                "Tibetan": {
                    'Word': "",
                    'phonetic': "",
                    'Sentence': ""
                },
                "czech": {
                    'Word': "",
                    'Sentence': ""
                },
                "meta_data": {
                    "Comment": "",
                    "Source": ""
                },
                "Message": "Success"
        },
        "Message": "Success",
        "Response": 200
    }
```

## Implementation Details
Note: **Taking website example as VOT**
### extract_all_vot_article Function
- Purpose: Extracts all article links from a given VOT webpage
- Input: URL of the VOT webpage categories 
- Output: Dictionary containing a list of article links, status message, and response code

### scrape_vot_article Function
- Purpose: Scrapes detailed information from a single VOT article
- Input: URL of the specific VOT news article
- Output: Dictionary containing article data (title, body, metadata), status message, and response code

### Key Features
- User-Agent header to mimic browser requests
- Error handling for various scenarios (timeout, request exceptions, parsing errors)
- Extraction of article title, author, date, tags, text content, and audio source (if available)

## Implementation Notes
- The current implementation focuses on the VOT website. Extend the code to handle other **Tibetan news websites.**
- Ensure that the scraping script respects each website's and implements appropriate delays between requests.
- Implement error logging to track any issues during the scraping process.
- Consider implementing incremental scraping to avoid duplicating content and to efficiently update the dataset over time.


## Resources
- Beautiful Soup library for HTML parsing
   - https://beautiful-soup-4.readthedocs.io/en/latest/
   - https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
   - https://realpython.com/beautiful-soup-web-scraper-python/
   - https://stackabuse.com/guide-to-parsing-html-with-beautifulsoup-in-python/
- Requests library for making HTTP requests
- Time library for implementing delays and tracking request duration
- https://www.youtube.com/watch?v=4tAp9Lu0eDI