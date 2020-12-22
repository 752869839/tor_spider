# -*- coding: utf-8 -*-
import json
import scrapy
import langid
import chardet
import random
import logging
import urllib.parse
from datetime import datetime
from scrapy import Request
from tor_spider.items import HtmlItem
logger = logging.getLogger(__name__)

class DarkSpider(scrapy.Spider):
    name = 'onion_guns_market_spider'
    # allowed_domains = ['gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion']
    start_urls = ['http://gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion/all.php']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        },
        'ITEM_PIPELINES': {
            'tor_spider.pipelines.TorDataPipeline': 188,
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.Guns_LoginMiddleware': 100,
            'tor_spider.middlewares.Guns_CookieMiddleware': 400,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY' : random.randint(5,15 )
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//figure[@class="cap-left stealth cap-top"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            # logger.info('商品列表url')
            # logger.info(list_url)
            yield Request(list_url, callback=self.parse_second,meta={'item': item})

    def parse_second(self, response):
        logger.info('商品详情链接')
        logger.info(response.url)
        logger.info('响应状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        try:
            view_urls = response.xpath('//tr[4]/td[3]/span[2]/a/@href').extract()
            for view_url in view_urls:
                view_url = response.urljoin(view_url)
                # logger.info('商品评论链接')
                # logger.info(view_url)
                yield Request(view_url, callback=self.parse_third, meta={'item': item})
        except Exception as e:
            pass

    def parse_third(self, response):
        logger.info('商品评论链接')
        logger.info(response.url)
        logger.info('响应状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item
