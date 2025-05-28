# Tibetan News Article Scraping

## Objective
Develop scripts to efficiently scrape Tibetan news articles from multiple sources and store them in a structured format for training machine translation models. This repository maintains a standardized record of every news article and website scraped to date—both text and audio.

## Repository Structure
```
tibetan-news-article-scraping/
├── News_Articles/
│   ├── in_india_website/
│   │   ├── Bangchen/
│   │   ├── RFA/
│   │   ├── VOATibetan/
│   │   ├── VOT/
│   │   ├── bod_asia/
│   │   ├── gyalwarinpoche/
│   │   └── tibetTimes/
│   └── in_tibet_website/
│   │   ├── kangbatv/
│   │   ├── kbcmw/
│   │   ├── khabdha/
│   │   ├── sertha/
│   │   ├── shangri-latibet/
│   │   ├── tb.tibet.cn/
│   │   ├── tb.xzxw/
│   │   ├── tb1025/
│   │   ├── tbmgar/
│   │   ├── tbwriters/
│   │   ├── teducn/
│   │   ├── tibetcm/
│   │   ├── tibetcnr/
│   │   ├── xizang.news/
│   │   ├── zangdiyg/
├── Web Translation/
│   ├── glosbe/
│   └── linguatools/
├── wikipedia/
├── test code/
└── README.md
```

## Data Storage Locations
All scraped data is stored in two locations:

1. **Repository**: Organized by region and website in the `News_Articles` directory
2. **AWS S3 Bucket**: 
   - Bucket: `s3://tibetan-news-data/`

## Scraped News Sources

| Source | Region | Media Type | Repository Path | S3 Path | Last Updated |
|--------|--------|------------|----------------|---------|--------------|
| Voice of Tibet (VOT) | India | Text, Audio | `News_Articles/in_india_website/VOT/` | `s3://openpecha-tibetan-news/india/vot/` | 2025-05-27 |
| Radio Free Asia (RFA) | India | Text, Audio | `News_Articles/in_india_website/RFA/` | `s3://openpecha-tibetan-news/india/rfa/` | 2025-03-21 |
| VOA Tibetan | India | Text, Audio | `News_Articles/in_india_website/VOATibetan/` | `s3://openpecha-tibetan-news/india/voatibetan/` | 2025-03-21 |
| Tibet Times | India | Text | `News_Articles/in_india_website/tibetTimes/` | `s3://openpecha-tibetan-news/india/tibettimes/` | 2024-09-05 |
| Bangchen | India | Text | `News_Articles/in_india_website/Bangchen/` | `s3://openpecha-tibetan-news/india/bangchen/` | 2024-09-03 |
| Gyalwa Rinpoche | India | Text | `News_Articles/in_india_website/gyalwarinpoche/` | `s3://openpecha-tibetan-news/india/gyalwarinpoche/` | 2024-08-22 |
| Bod Asia | India | Text | `News_Articles/in_india_website/bod_asia/` | `s3://openpecha-tibetan-news/india/bod_asia/` | 2024-08-20 |

## Data Structure
The scraped article links for each page are stored in a dictionary with the following structure:
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

## Tibetan News Websites Implemented
- https://vot.org/ (implemented)
    - Audio related to the article
- https://tibettimes.net/ (implemented)
    - No Audio
- https://www.voatibetan.com/ (implemented)
    - Audio not that related
- https://www.rfa.org/tibetan (implemented)
    - Audio Seems related
- http://bangchen.net/ (dead site)
- http://bangchen.tibetexpress.net (implemented)
    - No Audio
- https://www.gyalwarinpoche.com/ (implemented)
    - No Audio
- https://bod.asia/ (implemented)

## Tibetan to English Translation Websites Implemented
- https://linguatools.info/ (implemented)
- https://app.glosbe.com/ (implemented)

## Implementation Details

### Article Link Extraction
- **Purpose**: Extracts all article links from a given website's page
- **Input**: URL of the webpage categories 
- **Output**: Dictionary containing a list of article links, status message, and response code

### Article Content Scraping
- **Purpose**: Scrapes detailed information from a single article
- **Input**: URL of the specific news article
- **Output**: Dictionary containing article data (title, body, metadata), status message, and response code

### Key Features
- User-Agent header to mimic browser requests
- Error handling for various scenarios (timeout, request exceptions, parsing errors)
- Extraction of article title, author, date, tags, text content, and audio source (if available)

## Metadata Management
To maintain a standardized record of all scraped sources, we use a metadata system that tracks:

1. **Source categorization**:
   - Region (India, Tibet, etc.)
   - Language (Tibetan, English, etc.)
   - Media type (Text, Audio, Both)

2. **Storage locations**:
   - Repository path
   - S3 bucket path
   - File formats (.json, .mp3, etc.)

3. **Scraping history**:
   - Last scraped date (YYYY-MM-DD format)
   - Total articles scraped
   - Date range of articles

## Resources
- Beautiful Soup library for HTML parsing
   - https://beautiful-soup-4.readthedocs.io/en/latest/
   - https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
   - https://realpython.com/beautiful-soup-web-scraper-python/
   - https://stackabuse.com/guide-to-parsing-html-with-beautifulsoup-in-python/
- Requests library for making HTTP requests
- Time library for implementing delays and tracking request duration