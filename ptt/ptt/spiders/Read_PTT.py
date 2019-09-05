#-*-Coding: utf-8 -*-
import scrapy,jieba,pymysql
from ptt.items import PttItem
from datetime import datetime
class PttScrapy(scrapy.Spider):
    #爬蟲唯一識別碼
    name = "ptt"

    #爬蟲爬取網頁起始點
    start_urls = ['https://www.ptt.cc/bbs/CVS/index2183.html']

    def parse(self, response):
        #分析資料
        for ptt_title in response.css('.r-ent > div.title'):

            title = ptt_title.css(' a::text').extract()

            if(title[0][:4]=="[商品]"):

                href = ptt_title.css('a::attr(href)').extract()

                #取得網址
                url = response.urljoin(href[0])

                yield  scrapy.Request(url,callback=self.parse_article)

    def parse_article(self,response):
        item = PttItem()
        # 網址
        item['url'] = response.request.url

        #標題
        title = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
        item['title'] = title

        #發文時間
        datetime_str = response.xpath(
            '//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[0].extract()
        date = datetime.strptime(datetime_str,'%a %b %d %H:%M:%S %Y')
        item['date'] = date

        #get reply Year
        #轉時間戳記後取年分
        reply_year = date.timetuple().tm_year

        #內文
        item['content'] = response.xpath('//div[@id="main-content"]/text()')[0].extract()

        #解析
        start = 10
        for c, word in enumerate(item['content']):
            if (word == '【'):

                if (item['content'][start - 4:start - 2] == "價格"):

                    item['product'] = item['content'][start:c]

                if(item['content'][start - 4:start - 2] == "名稱"):

                    item['store'] = item['content'][start:c]

            if (word == '：'):

                start = c + 1

        reply = []
        for comments in response.xpath('//div[@class="push"]'):
            #推
            push_tag = comments.css('span.push-tag::text')[0].extract()

            #回覆內容
            push_content = comments.css('span.push-content::text')[0].extract()
            #回覆時間
            reply_str = comments.css('span.push-ipdatetime::text')[0].extract()

            #'09/04 14:56'
            reply_datetime = reply_str.lstrip()

            push_content_time = str(reply_year)+"/"+reply_datetime
            reply.append({
                'nrec' : push_tag,
                "reply" : push_content,
                "reply_date" : push_content_time
            })
        item['comments'] = reply
        for row in item['comments']:
            print(row['reply'])

        yield item
