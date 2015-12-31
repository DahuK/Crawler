#-*- coding: UTF-8 -*- 
import re

from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor  
from scrapy.contrib.spiders import Rule, CrawlSpider  
from scrapy.http import Request
from scrapy.selector import Selector  

from jd.items import JdbookItem


class JDSpider(CrawlSpider):  
    name = "jd"  
    allowed_domains = ["jd.com"]  
    start_urls = [  
                    "http://list.jd.com/list.html?cat=1713,3287,3797"
    ]

    def printhxs(hxs): 
        for i in hxs: 
            print i.encode('utf-8')
            
    def parse_item_url(response):
        #itemurl = response.xpath("//div[@id='choose-color']/div[2]/div")
        print 'IIIIIIIII'
        item = JdbookItem()
        itemurl = response.xpath("//*[@id='product-intro']")
        item['name']= response.xpath("//*[@id='name']/h1/text()").extract()[0].encode('utf-8')
        
        print item['name']
        
        return item
#         for url in itemurl.xpath("//*[@id='itemInfo'']").extract():
#             item = JdbookItem()
#             item['name'] = url.xpath("//*[@id='name']/h1/text()").extract()
#             
#                         
#             i = i + 1
#             r = Request(url, callback= parseDetail)
#             r.meta['item'] = item
#             yield r
    
    def parse_next_page(response):
        sel = Selector(response)
        pages_num = sel.xpath("//*[@id='J_bottomPage']/span[2]/em[1]/b/text()")  
        
        page_url = sel.xpath("//*[@id='J_bottomPage']/span[1]/a[2]/@href").extract()
        #/list.html?cat=1713,3287,3797&ev=12753_136338&page=1&go=0&JL=6_0_0
        PAGE_PATTERN = r'(.+page=)[\d]+(.+)'
        parse = re.compile(PAGE_PATTERN, re.UNICODE|re.VERBOSE)
        match = parse.search(page_url)
        if match:
            pre_url = match.group(1)
            post_url = match.group(2)
            
            for i in xrange(2, int(pages_num)+1):
                
                page_url = pre_url+ str(i) + post_url
                r = Request(page_url, callback = parse_detail)
                sel = Selector(response)
                return
        else:
            print 'NONONONO!'

    
    def parse_detail(response):
        sel = Selector(response)
        book_element = sel.xpath("//div[@class='tab-content-item j-sku-item tab-cnt-i-selected']")
        if book_element is None:
            book_element = sel.xpath("//div") 
        item = JdbookItem()
        item['name'] = book_element.xpath('/div[3]/a/em/text()').extract().encode('utf-8')  
        item['price'] = book_element.xpath('/div[2]/strong/i/text()').extract().encode('utf-8')
        item['publisher'] = book_element.xpath('/div[4]/span[2]/a/text()').extract().encode('utf-8') 
        item['author'] = book_element.xpath('/div[4]/span[1]/span[1]/a[1]/text()').extract().encode('utf-8')
        item['commit'] = book_element.xpath('/div[6]/strong/a/text()').extract().encode('utf-8') 
        item['shop'] = book_element.xpath('/div[7]/span/text()').extract().encode('utf-8')
        return item
        
    rules = [        
#         Rule(LxmlLinkExtractor(allow=("list.html?cat=1713,3287,3797&ev=12753_136338@&page=1&JL=3_%E7%A8%8B%E5%BA%8F%E7%B1%BB%E5%9E%8B_Java"), restrict_xpaths=("//a[@class='next']")), follow=True),  
#         Rule(LxmlLinkExtractor(allow=("/\d{8}.html")), callback=parseItemurl)
        
        Rule(LxmlLinkExtractor(allow=("list.html?cat=1713,3287,3797&ev=12753_136338@&page=1&JL=3_%E7%A8%8B%E5%BA%8F%E7%B1%BB%E5%9E%8B_Java"), restrict_xpaths=("//a[@class='next']")), follow=True),
        Rule(LxmlLinkExtractor(allow=("//*[@id='plist']/ul/li[\d+]"), callback=parse_detail),
        Rule(LxmlLinkExtractor(allow=("//*[@id='J_bottomPage']")), callback=parse_next_page)
    ]

    def parsePrice(response):  
        sel = Selector(text=response.body)  
        try:  
            price = sel.xpath("//text()").extract()[0].encode('utf-8').split('"')[7]  
        except Exception, ex:  
            print ex;  
            price = 0  
        item = response.meta['item']  
        item['price'] = price   
        return item
        
        
