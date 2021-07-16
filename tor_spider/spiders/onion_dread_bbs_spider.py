# -*- coding: utf-8 -*-
import json
import scrapy
import chardet
import langid
import logging
import urllib.parse
from scrapy import Request
from datetime import datetime
from tor_spider.items import HtmlItem

logger = logging.getLogger(__name__)
class DarkSpider(scrapy.Spider):
    name = 'onion_dread_bbs_spider'
    # allowed_domains = ['dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/']
    start_urls = ['http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Host': 'dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion',
            'Referer': 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'dcap=1C5A2D4B35F1F5DC8548690F1AF5D7CD92AC622B232DD4831D3A8BC799ECFA1A55FFF45059D9EFFA40448317937D16567FEDBA30C28F9AB8BB0A2F130A07E528; dread=k21jjhcsurm4qq6k0qnkad4t25',
        },
        'ITEM_PIPELINES' : {
            'tor_spider.pipelines.TorDataPipeline': 188,
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
},
        'DOWNLOADER_MIDDLEWARES': {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//nav[@class="subdreadQuick"]/ul/li/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'首页链接:{list_url}')
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    def parse_sencond(self, response):
        logger.info(f'请求状态码:{response.status}')
        item = response.meta['item']
        list_urls = response.xpath('//div[@class="postTop"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'帖子链接:{list_url}')
            yield Request(list_url, callback=self.parse_third, meta={'item': item})

        try:
            next_page = response.xpath('//a[text()="Next"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info(f'翻页链接:{next_page}')
            yield Request(next_page, callback=self.parse_sencond, meta={'item': item})
        except Exception as e:
            pass

    def parse_third(self,response):
        logger.info(f'请求状态码:{response.status}')
        item = response.meta['item']
        imgs = response.xpath('//img/@src').extract()
        if len(imgs) > 0:
            l_img = []
            for i in imgs:
                img = response.urljoin(i)
                l_img.append(img)
            item['img'] = l_img
            item['html'] = str(response.body, encoding='utf-8')
        else:
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



