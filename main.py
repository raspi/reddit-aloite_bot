import json
import logging
import os
import sys
import urllib

import praw
from praw.exceptions import APIException

VERSION = "1.0.0"
BOTNAME = f"aloite_bot v{VERSION}"


class AloiteBot:
    _name = BOTNAME
    bot = None
    subname = None
    urls_cache = []
    cachefile = None
    log = None

    def __init__(self):
        if self.subname is None:
            raise ValueError("sub name not set")

        self.log = logging.getLogger(__name__)

        data = {}
        with open("auth.json", "r", encoding="utf8") as f:
            data = json.load(f)

        self.bot = praw.Reddit(client_id=data["clientid"],
                               client_secret=data["secret"],
                               password=data["password"],
                               username=data["username"],
                               user_agent=self._name,
                               )
        self.cachefile = f"{self.subname}.cache"
        self.loadCache()

    def submit(self, title: str, url: str):
        self.log.info(f"{self.subname}: {title} - {url}")
        res = self.bot.subreddit(self.subname).submit(title, url=url, resubmit=False)
        return res

    def loadResource(self):
        raise NotImplementedError()

    def cacheUrl(self, url: str):
        self.log.info(f"caching {url}")
        with open(self.cachefile, "a+", encoding="utf8") as f:
            f.write(url + "\n")

    def loadCache(self):
        self.log.info("loading cache..")
        lines = []
        if not os.path.isfile(self.cachefile):
            return

        with open(self.cachefile, "r", encoding="utf8") as f:
            lines = f.readlines()

        self.urls_cache = list(map(str.strip, lines))


class JsonResourceBot(AloiteBot):
    _sourceurl = None

    def loadJson(self) -> list:
        data = None

        with urllib.request.urlopen(self._sourceurl) as response:
            if response.code != 200:
                raise ValueError("url couldn't be loaded")
            if response.headers.get_content_type() != "application/json":
                raise ValueError("invalid content type")
            data = json.loads(response.read())

            if not isinstance(data, list):
                raise KeyError("not list")

        return data


class KuntalaisAloiteBot(JsonResourceBot):
    subname = "kuntalaisaloite"
    _sourceurl = "https://www.kuntalaisaloite.fi/api/v1/initiatives?orderBy=latest"

    def loadResource(self):
        data = self.loadJson()

        for item in data:
            title = f"[{item['municipality']['nameFi']}] {item['name']}"
            url = item["url"]["fi"]

            if url in self.urls_cache:
                self.log.info(f"url exists in cache, skipping: {url}")
                continue

            try:
                subres = self.submit(title, url)
            except APIException as e:
                if e.error_type == "ALREADY_SUB":
                    self.cacheUrl(url)
                    continue
                raise


class KansalaisAloiteBot(JsonResourceBot):
    subname = "kansalaisaloite"
    _sourceurl = "https://www.kansalaisaloite.fi/api/v1/initiatives?orderBy=mostTimeLeft"

    def loadResource(self):
        data = self.loadJson()

        for item in data:
            title = item['name']['fi']
            url = item["url"]["fi"]

            if url in self.urls_cache:
                self.log.info(f"url exists in cache, skipping: {url}")
                continue

            try:
                subres = self.submit(title, url)
            except APIException as e:
                if e.error_type == "ALREADY_SUB":
                    self.cacheUrl(url)
                    continue
                raise


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s: %(message)s",
        level=logging.INFO,
    )

    log = logging.getLogger(__name__)

    had_errors = False

    try:
        bot = KansalaisAloiteBot()
        bot.loadResource()
    except Exception as e:
        had_errors = True
        log.error(e)

    try:
        bot = KuntalaisAloiteBot()
        bot.loadResource()
    except Exception as e:
        had_errors = True
        log.error(e)

    if had_errors:
        sys.exit(1)
