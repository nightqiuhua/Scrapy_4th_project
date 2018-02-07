# -*- coding: utf-8 -*-
import scrapy
import re
from Tencent_3.items import Tencent3Item

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "https://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [baseURL + str(offset)]
    link_regx ='position.php\?&start'
    seen = set()
    crawl_queue = [baseURL]

    def parse(self, response):
        node_list = response.xpath('//tr[@class="odd"]|//tr[@class="even"]')
        for node in node_list:
            item = Tencent3Item()
            item['position_name'] = node.xpath('./td[1]/a/text()').extract()[0]
            item['position_link'] = node.xpath('./td[1]/a/@href').extract()[0]
            if len(node.xpath('./td[2]/text()')):
                item['position_type'] = node.xpath('./td[2]/text()').extract()[0]
            else:
                item['position_type'] =" "
            item['position_num'] = node.xpath('./td[3]/text()').extract()[0]
            item['workplace'] = node.xpath('./td[4]/text()').extract()[0]
            item['publishtime'] = node.xpath('./td[5]/text()').extract()[0]

            yield item

        raw_links = []
        links = []
        raw_links = response.xpath('//tr[@class="f"]/td/div[2]/div/a/@href').extract()
        links.extend(link for link in raw_links if re.match(self.link_regx,link))

        for link in links:
            link = 'https://hr.tencent.com/'+link
            if link not in self.seen:
                self.seen.add(link)
                self.crawl_queue.append(link)

        url = self.crawl_queue.pop()
        try:
            yield scrapy.Request(url,callback = self.parse)
        except Exception as e:
            print('crawl finish')



        #if self.offset < 500:
        #    self.offset += 10
        #    url = self.baseURL + str(self.offset)
        #    yield scrapy.Request(url,callback = self.parse)
        #    
        #    

        #while crawl_queue:
        #    url = crawl_queue.pop()
        #    yield scrapy.Request(url,callback = self.parse)
        #    raw_links = []
        #    raw_links = response.xpath('//tr[@class="f"]/td/div[2]/div/a/@href').extract()
        #    links.extend(link for link in raw_links if re.match(link_regx,link))

        #    for link in links:
        #        link = 'https://hr.tencent.com/'+link
        #        if link not in seen:
        #            seen.add(link)
        #            crawl_queue.append(link)


        #if len(response.xpath('//a[@id="next" and @class="noactive"]')) ==0:
        #    url = "https://hr.tencent.com/"+response.xpath('//a[@id="next"]/@href').extract()[0]
        #    yield scrapy.Request(url,callback = self.parse)
