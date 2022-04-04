import scrapy
import os

base_url = 'https://hd.hainanu.edu.cn/cs/'
class HainanSpider(scrapy.Spider):
    name = 'hainan'
    allowed_domains = ['hainanu.edu.cn']

    start_urls = ['https://hd.hainanu.edu.cn/cs/yjsjy/xxgg.htm']

    def parse(self, response):
        li = response.xpath("/html/body/div[2]/div/dl[2]/div[2]/div[1]/ul/li")
        for a in li:
            surl = a.xpath("./span/a/@href").extract_first().split('../')[-1]
            yield scrapy.Request(
                url = base_url + surl,
                callback = self.detail
            )

    def detail(self, response):
        title = response.xpath("/html/body/div[2]/div/dl/div[2]/form/div[1]/ul/h1/text()").extract_first()
        time = response.xpath("/html/body/div[2]/div/dl/div[2]/form/div[1]/ol/text()").extract_first()
        try:
            os.system(
                "python3 /home/ubuntu/nonebot/mail.py -t '{t}' -m '{m}'".format(t='海大通知', m='<h1>{title}</h1></br>发布时间：<strong>{time}</strong>'.format(title=title,time=time)))
        except Exception as e:
            print(e)