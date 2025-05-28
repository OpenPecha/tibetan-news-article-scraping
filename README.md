# Tibetan News Article Scraping

## Objective
Develop scripts to efficiently scrape Tibetan news articles from multiple sources and store them in a structured format for training machine translation models. This repository maintains a standardized record of every news article and website scraped to date—both text and audio.

## Description
We need Tibetan news articles for training our machine translation model. This task involves creating scripts to collect articles from various Tibetan news websites and organizing them in a clear, structured format.

## Data Storage Locations
All scraped data is stored in two locations:

1. **Repository**: Organized by region and website in the `News_Articles` directory
2. **AWS S3 Bucket**: For long-term storage and larger audio files
   - Bucket: 
   - `s3://tibetan-news-data/` [Primary storage for news articles]
   - `s3://voa-rfa-data/` [Dedicated storage for VOA and RFA content]
3. **File formats:** `.json` for articles, `.mp3` for audio

   

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
│       ├── kangbatv/
│       ├── kbcmw/
│       ├── khabdha/
│       ├── sertha/
│       ├── shangri-latibet/
│       ├── tb.tibet.cn/
│       ├── tb.xzxw/
│       ├── tb1025/
│       ├── tbmgar/
│       ├── tbwriters/
│       ├── teducn/
│       ├── tibetcm/
│       ├── tibetcnr/
│       ├── xizang.news/
│       └── zangdiyg/
├── Web Translation/
│   ├── glosbe/
│   └── linguatools/
├── wikipedia/
├── test code/
│   ├── convert_all_unix_json.ipynb
│   └── scraping_audio_data/
└── README.md
```

## Scraped News Sources
|Source               |Region|Media Type |Repository Path                                  |S3 Path                                                    |Last Updated|Website                         |
|---------------------|------|-----------|-------------------------------------------------|-----------------------------------------------------------|------------|--------------------------------|
|Voice of Tibet (VOT) |India |Text, Audio(not downloaded)|`News_Articles/in_india_website/VOT/`            |`s3://tibetan-news-data/News Article/vot/` |22-08-2024  |https://vot.org/                |
|Radio Free Asia (RFA)|India |Text, Audio|`News_Articles/in_india_website/RFA/`            |`s3://voa-rfa-data/RFA_Tibetan/`                 |27-03-2025  |https://www.rfa.org/tibetan     |
|VOA Tibetan          |India |Text, Audio|`News_Articles/in_india_website/VOATibetan/`     |`s3://voa-rfa-data/VOA_Tibetan/`          |27-03-2025  |https://www.voatibetan.com/     |
|Tibet Times          |India |Text       |`News_Articles/in_india_website/tibetTimes/`     |`s3://tibetan-news-data/News Article/tibettimes/`          |22-08-2024  |https://tibettimes.net/         |
|Bangchen             |India |Text       |`News_Articles/in_india_website/Bangchen/`       |`s3://tibetan-news-data/News Article/bangchen/`            |22-08-2024  |http://bangchen.tibetexpress.net|
|Gyalwa Rinpoche      |India |Text       |`News_Articles/in_india_website/gyalwarinpoche/` |`s3://tibetan-news-data/News Article/gyalwarinpoche/`      |22-08-2024  |https://www.gyalwarinpoche.com/ |
|Bod Asia             |India |Text       |`News_Articles/in_india_website/bod_asia/`       |`s3://tibetan-news-data/News Article/bod_asia/`            |03-09-2024  |https://bod.asia/               |
|Kangba TV            |Tibet |Text       |`News_Articles/in_tibet_website/kangbatv/`       |`s3://tibetan-news-data/new_news_Articles/kangbatv/`       |20-09-2024  |http://www.kangbatv.com/        |
|KBCMW                |Tibet |Text       |`News_Articles/in_tibet_website/kbcmw/`          |`s3://tibetan-news-data/new_news_Articles/kbcmw/`          |20-09-2024  |http://www.kbcmw.com/           |
|Khabdha              |Tibet |Text       |`News_Articles/in_tibet_website/khabdha/`        |`s3://tibetan-news-data/new_news_Articles/khabdha/`        |20-09-2024  |http://www.khabdha.org/         |
|Sertha               |Tibet |Text       |`News_Articles/in_tibet_website/sertha/`         |`s3://tibetan-news-data/new_news_Articles/sertha/`         |20-09-2024  |http://www.sertha.org/          |
|Shangri-la Tibet     |Tibet |Text       |`News_Articles/in_tibet_website/shangri-latibet/`|`s3://tibetan-news-data/new_news_Articles/shangri-latibet/`|20-09-2024  |http://www.shangri-latibet.org/ |
|Tibet.cn             |Tibet |Text       |`News_Articles/in_tibet_website/tb.tibet.cn/`    |`s3://tibetan-news-data/new_news_Articles/tb-tibet-cn/`    |20-09-2024  |http://tb.tibet.cn/             |
|XZXW                 |Tibet |Text       |`News_Articles/in_tibet_website/tb.xzxw/`        |`s3://tibetan-news-data/new_news_Articles/tb-xzxw/`        |20-09-2024  |http://tb.xzxw.com/             |
|TB1025               |Tibet |Text       |`News_Articles/in_tibet_website/tb1025/`         |`s3://tibetan-news-data/new_news_Articles/tb1025/`         |20-09-2024  |http://tb.1025.cn/              |
|TB MGAR              |Tibet |Text       |`News_Articles/in_tibet_website/tbmgar/`         |`s3://tibetan-news-data/new_news_Articles/tbmgar/`         |20-09-2024  |http://tb.mgar.com/             |
|TB Writers           |Tibet |Text       |`News_Articles/in_tibet_website/tbwriters/`      |`s3://tibetan-news-data/new_news_Articles/tbwriters/`      |30-09-2024  |http://tb.writers.com/          |
|Tibet Education      |Tibet |Text       |`News_Articles/in_tibet_website/teducn/`         |`s3://tibetan-news-data/new_news_Articles/teducn/`         |30-09-2024  |http://www.teducn.com/          |
|Tibet CM             |Tibet |Text       |`News_Articles/in_tibet_website/tibetcm/`        |`s3://tibetan-news-data/new_news_Articles/tibetcm/`        |20-09-2024  |http://www.tibetcm.com/         |
|Tibet CNR            |Tibet |Text       |`News_Articles/in_tibet_website/tibetcnr/`       |`s3://tibetan-news-data/new_news_Articles/tibetcnr/`       |20-09-2024  |http://www.tibetcnr.com/        |
|Xizang News          |Tibet |Text       |`News_Articles/in_tibet_website/xizang.news/`    |`s3://tibetan-news-data/new_news_Articles/xizang-news/`    |20-09-2024  |http://www.xizang.news/         |
|Zang DIYG            |Tibet |Text       |`News_Articles/in_tibet_website/zangdiyg/`       |`s3://tibetan-news-data/new_news_Articles/zangdiyg/`       |20-09-2024  |http://www.zangdiyg.com/        |


## Translation Resources

| Source | Type | Repository Path | S3 Path | Last Updated |
|--------|------|----------------|---------|--------------|
| Glosbe | Translation | `Web Translation/glosbe/` | `s3://tibetan-news-data/Web Translation/glosbe/` | 2024-09-05 |
| Lingua Tools | Translation | `Web Translation/linguatools/` | `s3://tibetan-news-data/Web Translation/linguatools/` | 2024-08-31 |

## Wikipedia Resources

| Source | Type | Repository Path | S3 Path | Last Updated |
|--------|------|----------------|---------|--------------|
| Wikipedia | Encyclopedia | `wikipedia/` | `s3://tibetan-news-data/new_news_Articles/wikipedia/` | 2024-09-26 |

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