#-*- coding: UTF-8 -*- 
import re

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor  
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector  
from scrapy.selector.lxmlsel import HtmlXPathSelector

from jd.items import JdbookItem


class JDSpider(CrawlSpider):  
    name = "jd"  
    allowed_domains = ["jd.com"]  
    start_urls = [
        "http://list.jd.com/list.html?cat=1713,3287,3797"
   #     "http://list.jd.com/list.html?cat=1713,3287,3797&ev=12753%5F136338&go=0&JL=3_%E7%A8%8B%E5%BA%8F%E7%B1%BB%E5%9E%8B_Java"
    ]
     
    def printhxs(self, hxs): 
        for i in hxs: 
            print i.encode('utf-8')
            
    def parse_item_url(self, response):
        #itemurl = response.xpath("//div[@id='choose-color']/div[2]/div")
        print 'IIIIIIIII'
        item = JdbookItem()
        itemurl = response.xpath("//*[@id='product-intro']")
        item['name']= response.xpath("//*[@id='name']/h1/text()").extract()[0].encode('utf-8')
        
        print item['name']
        
        return item
    
    def parse_next_page(self, response):
        print("Fetch group home page: %s" % response.url)
 
        hxs = HtmlXPathSelector(response)
        
        pages_num = hxs.select("//*[@id='J_bottomPage']/span[2]/em[1]/b/text()").extract()[0]
        print pages_num
        page_url = hxs.select("//*[@id='J_bottomPage']/span[1]/a[2]/@href").extract()[0]
        print page_url
        PAGE_PATTERN = r'(.+page=)[\d]+(.+)'
        parse = re.compile(PAGE_PATTERN, re.UNICODE|re.VERBOSE)
        match = parse.search(page_url)
        if match:
            
            pre_url = match.group(1)
            post_url = match.group(2)
            
            for i in xrange(2, int(pages_num)+1):
                #iterate each page
                page_url = 'http://list.jd.com' + pre_url+ str(i) + post_url
                print page_url + ' ??????????????????'
                r = Request(page_url, callback = self.parse_detail)
                yield r 
        else:
            print 'NONONONO!'

    
    def parse_detail(self, response):
        print '--------------------------'
        self.logger.info('--------------------------')
        hxs = HtmlXPathSelector(response)
        print str(len(hxs.xpath("//*[@id='plist']/ul/li[@class='gl-item']"))) + ' CCCCCCCCCCCCC' 
        items = []
        for gl_item in hxs.xpath("//*[@id='plist']/ul/li[@class='gl-item']"):
            #self.logger.info("GGGGGGGGGGGGGGGGGGGGGGGGG: %s" % gl_item.extract())

            book_element = gl_item.xpath("div[@class='tab-content-item j-sku-item tab-cnt-i-selected']")
            if book_element is None or len(book_element) == 0:
                book_element = gl_item.xpath("div")                 
            item = JdbookItem()
            item['name'] = book_element.xpath('div[3]/a/em/text()').extract()[0].encode('utf-8')  
            print book_element.xpath('div[2]/strong/i').extract()[0] + ' >>>>>>>>>>>>>>>'
          # item['price'] = book_element.xpath('div[2]/strong/i/text()').extract()[0].encode('utf-8')
            item['publisher'] = book_element.xpath('div[4]/span[2]/a/text()').extract()[0].encode('utf-8') 
            item['author'] = book_element.xpath('div[4]/span[1]/span[1]/a[1]/text()').extract()[0].encode('utf-8')
            item['commit'] = book_element.xpath('div[6]/strong/a/text()').extract()[0].encode('utf-8') 
            item['shop'] = book_element.xpath('div[7]/span/text()').extract()[0].encode('utf-8')
#             response.meta['item'] = item
#             yield response
            items.append(item)
        return items
            
    rules = [                 
#         Rule(LxmlLinkExtractor(allow=("list.html?cat=1713,3287,3797&ev=12753_136338@&page=1&JL=3_%E7%A8%8B%E5%BA%8F%E7%B1%BB%E5%9E%8B_Java"), restrict_xpaths=("//a[@class='next']")), follow=True),  
#         Rule(LxmlLinkExtractor(allow=("/\d{8}.html")), callback=parseItemurl)
#         Rule(LxmlLinkExtractor(restrict_xpaths=("//*[@id='J_bottomPage']/span[1]")), follow=True),
#         Rule(LxmlLinkExtractor(allow=("/\d{8}.html")), callback=parse_item_url)
#         Rule(LxmlLinkExtractor(allow=("//*[@id='plist']/ul/li[\d+]")), callback=parse_detail),
         Rule(LxmlLinkExtractor(allow=(r'^.+[Java]$'), restrict_xpaths=("//*[@id='J_selector']/div[4]/div/div[2]/div[1]/ul")), callback='parse_next_page')
    ]

    def parsePrice(self, response):  
        sel = Selector(text=response.body)  
        try:  
            price = sel.xpath("//text()").extract()[0].encode('utf-8').split('"')[7]  
        except Exception, ex:  
            print ex;  
            price = 0  
        item = response.meta['item']  
        item['price'] = price   
        return item
        
        
