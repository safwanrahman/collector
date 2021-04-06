import re
from functools import cached_property
import time

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options
from selenium import webdriver


class WebsiteScrapper:

    def __init__(self, website):
        self.website = website
        self.host = f"https://{website}"

    @cached_property
    def webdriver(self):
        options = Options()
        options.add_argument("--headless")
        firefox = webdriver.Firefox(options=options)
        return firefox

    @cached_property
    def _page_content(self):
        resp = requests.get(self.host)
        return resp.content

    @cached_property
    def _bs4_object(self):
        return BeautifulSoup(self._page_content, 'html.parser')

    def get_about_page_url(self):
        soup = self._bs4_object
        regex = re.compile("about", re.IGNORECASE)
        in_link = soup.find(href=regex)
        if in_link:
            return in_link["href"]

        # If not find in link, find out in string. It should be lower than finding in link
        in_string = soup.find_all("a", string=regex)
        if in_string:
            for tag in in_string:
                if tag.has_attr("href"):
                    return tag["href"]

    def get_url_or_none(self, name):
        obj = self._bs4_object.find('a', href=re.compile(name))
        if obj:
            return obj["href"]

    @cached_property
    def social_media_urls(self):
        data = {
            "facebook": self.get_url_or_none("facebook"),
            "twitter": self.get_url_or_none("twitter"),
            "linkedin": self.get_url_or_none("linkedin")
        }
        return data

    def get_twitter_url(self):
        return self.social_media_urls["twitter"]

    def get_about_page_data(self):
        url = self.get_about_page_url()
        if url:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content, 'html.parser')
            data = []
            for tag in soup.find_all("p", string=True):
                if tag.string != "\xa0":
                    data.append(tag.string)

            return data

    def get_website_data(self):
        data = {
            "about": self.get_about_page_data(),
            "social_medias": self.social_media_urls
        }
        return data

    def get_twitter_page_content(self):
        url = self.get_twitter_url()
        if url:
            webdriver = self.webdriver
            webdriver.get(url)
            time.sleep(5)
            return webdriver.page_source

    def get_twitter_data(self):
        content = self.get_twitter_page_content()
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            data = dict()
            data["following"] = soup.find(href=re.compile("following")).contents[0].string
            data["followers"] = soup.find(href=re.compile("followers")).contents[0].string
            data["about"] = soup.find(attrs={"data-testid": "UserDescription"}).contents[0].string
            items = soup.find(attrs={"data-testid": "UserProfileHeader_Items"}).contents
            data["location"] = items[0].text
            data["joined"] = items[2].text
            return data
