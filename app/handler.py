import json
from urllib.parse import urlparse

from .documents import search_index, WebsiteDocument, TwitterDocument
from .scrapper import WebsiteScrapper


def get_or_create_processed_data(website):
    data = {"website": {},
            "twitter": {}
            }

    search = search_index.search().filter('term', host=website)
    result = search.execute()
    if result:
        for obj in result:
            obj_data = obj.to_dict()
            # Remove host from data
            del obj_data["host"]
            if obj.meta.index == WebsiteDocument._index._name:
                data["website"] = obj_data
            elif obj.meta.index == TwitterDocument._index._name:
                data["twitter"] = obj_data

        return data

    scrapper = WebsiteScrapper(website=website)
    website_data = scrapper.get_website_data()
    twitter_data = scrapper.get_twitter_data()
    web_doc = WebsiteDocument(host=website, **website_data)
    web_doc.save()
    if twitter_data:
        twitter_doc = TwitterDocument(host=website, link=scrapper.get_twitter_url(), **twitter_data)
        twitter_doc.save()

    data["website"] = website_data
    data["twitter"] = twitter_data
    return data


def get_or_create(event, context):
    try:
        data = json.loads(event['body'])
    except json.JSONDecoder:
        return {
            "statusCode": 400,
            "body": "Invalid json"
        }
    url = data.get("url")
    if not url:
        return {
            "statusCode": 400,
            "body": "No url"
        }

    website = urlparse(url).netloc
    data = get_or_create_processed_data(website)
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
