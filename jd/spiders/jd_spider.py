#-*- coding: UTF-8 -*- 
from scrapy.http import Request
from scrapy.selector import Selector  
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor  
from scrapy.contrib.spiders import Rule, CrawlSpider  
from jd.items import JdbookItem


class JDSpider(CrawlSpider):  
    name = "jd"  
    allowed_domains = ["jd.com"]  
    start_urls = [  
                    "http://list.jd.com/list.html?cat=1713,3287,3797"
    ]

    def parseItemurl(response):
        #itemurl = response.xpath("//div[@id='choose-color']/div[2]/div")
        print 'IIIIIIIII'
        itemurl = response.xpath("//div[@id='J_selector']/div[3]/div/div[2]/div[1]/ul")
        
        name = response.xpath("//*[@id='name']/h1")
        
        print itemurl
        i = 1
        for url in itemurl.xpath("a/@href").extract():
            item = JdbookItem()
            item['categoty'] = response.xpath("//div[@id='J_selector']/div[3]/div/div[2]/div[1]/ul/li[" + str(i) + "]/a/@title").extract()
            i = i + 1
            r = Request(url, callback= parseDetail)
            r.meta['item'] = item
            yield r
                
    rules = [  
   #     Rule(LxmlLinkExtractor(allow="/\d{8}.html"), callback=parseItemurl),
        
        Rule(LxmlLinkExtractor(allow=("list.html?cat=1713,3287,3797&ev=12753_136338@&page=1&JL=3_%E7%A8%8B%E5%BA%8F%E7%B1%BB%E5%9E%8B_Java"), restrict_xpaths=("//a[@class='next']")), follow=True),  
        Rule(LxmlLinkExtractor(allow=("/\d{8}.html")), callback=parseItemurl)
    ]

  
    def parseDetail(response):
#        mainurl = response.url
#        productid = mainurl[19:29]
#        priceUrl = 'http://p.3.cn/prices/mgets?skuIds=J_' + productid + 'J_'
#        
#        r = Request(priceUrl, callback=self.parsePrice)
#        sel = Selector(response)
#        # item = JdcoatItem()

        sel = Selector(response)
        product_detail = sel.xpath("//*[@id='plist']/ul")  
        i = 0  
        # 获取其他信息  
        elseInfo = ''  
#        for info in product_detail.xpath("text()").extract():              
#            infoList = info.encode('utf-8').split("：")  
#            # 获取店铺标签所在的位置  
#            i = i + 1  
#            key = infoList[0]  
#            value = infoList[1]  
#            if(key == "商品编号"):  
#                item['productID'] = value  
#            elif(key == "上架时间"):  
#                item['time'] = value  
#            elif(key == "店铺"):  
#                item['shop'] = sel.xpath("//ul[@class='detail-list']/li[" + str(i) + "]/a/text()").extract()  
#                item['shop_url'] = sel.xpath("//ul[@class='detail-list']/li[" + str(i) + "]/a/@href").extract()  
#            elif(key == "商品毛重"):  
#                item['weight'] = value  
#            elif(key == "商品产地"):  
#                item['addr'] = value  
#            elif(key == "尺码"):  
#                item['size'] = value  
#            elif(key == "材质"):  
#                item['material'] = value  
#            elif(key == "颜色"):  
#                item['color'] = value  
#            elif(key == "流行元素"):  
#                item['popEle'] = value  
#            elif(key == "上市时间"):  
#                item['marketTime'] = value  
#            elif(key == "袖型"):  
#                item['sleeves_type'] = value  
#            elif(key == "风格"):  
#                item['style'] = value  
#            elif(key == "版型"):  
#                item['version_type'] = value  
#            elif(key == "厚度"):  
#                item['thickness'] = value  
#            elif(key == "衣长"):  
#                item['length'] = value  
#            elif(key == "衣门襟"):  
#                item['yimenjin'] = value  
#            elif(key == "领型"):  
#                item['collar'] = value  
#            elif(key == "图案"):  
#                item['pattern'] = value  
#            else:  
#                if((key != "商品名称")):  
#                    elseInfo = elseInfo + info.encode('utf-8') + '~'  
#        item['elseInfo'] = elseInfo  
#        item['title'] = sel.xpath("//div[@id='name']/h1/text()").extract()  
#        item['category'] = sel.xpath("//div[@class='breadcrumb']/span[1]/a[2]/text()").extract()  
#        item['url'] = mainurl  
#        item['image_urls'] = sel.xpath("//div[@id='preview']/div/img/@src").extract()  
#        item['images'] = sel.xpath("//div[@id='product-intro']/div[3]/div[1]/img/@src").extract()  
#        r.meta['item'] = item  
#        return r  
    
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
        
        
