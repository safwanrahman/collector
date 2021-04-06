import os

from elasticsearch_dsl import Document, Keyword, Text, Integer, Index, Object

from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
elastic_host = os.environ.get("ELASTICSEARCH_HOST")
connections.create_connection(hosts=[elastic_host])


class WebsiteDocument(Document):
    host = Keyword()
    about = Text()
    social_medias = Object()

    class Index:
        name = "data-website"


class TwitterDocument(Document):
    host = Keyword()
    link = Keyword()
    following = Keyword()
    followers = Keyword()
    about = Text()
    location = Text()
    joined = Keyword()

    class Index:
        name = "data-twitter"


class FacebookDocument(Document):

    class Index:
        name = "data-facebook"


class LinkedinDocument(Document):
    class Index:
        name = "data-linkedin"


search_index = Index(name="data-*")
