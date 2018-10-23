# -*- coding: utf-8 -*-
import scrapy
import webbrowser
from pprint import pprint

class DoubanLoginSpider(scrapy.Spider):
    name = 'douban_login'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com']
    login_url = "https://www.douban.com/accounts/login"
    setting_url = 'https://www.douban.com/settings/notification'
    headers = {
        "User-Agent":"User-Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    }
    captcha_solution = None

    def login_parse(self, response):
        x = response.css("div.item.item-captcha img::attr(src)").extract()[0]
        if (x):
            print(x)
            print("验证码:")
            webbrowser.open_new_tab(x)
            self.captcha_solution = str(input())
            #print(len(self.captcha_solution),self.captcha_solution)
        formdata = {
            'source': 'index_nav',
            "form_email": "13697252729",
            "form_password": "451325378+",
            "captcha-solution": self.captcha_solution,
            "login": "登录"
        }
        return [scrapy.FormRequest.from_response(response, formdata=formdata,callback=self.parse_login)]

    def start_requests(self):
        yield scrapy.Request(self.login_url,headers=self.headers,callback=self.login_parse)

    def parse(self,response):
        pass

    def parse_login(self,response):
        if '登录豆瓣' in response.text:
            print("No!!!!!")
        else:
            print("Yes!")
            yield scrapy.Request(url=self.setting_url,callback=self.parse_setting)

    def parse_setting(self,response):
        if (response.url == self.setting_url):
            ck = response.css("div[style='display:none;'] input::attr(value)").extract()[0]
            fromdata={
                "ck": ck,
                "request": "request_forward",
                "dm": "dm_forward",
                "recv_weekly_rec": "sns:notification:recv_weekly_rec",
                "market": "market_no_forward",
                "notification": "notification_noforward",
                "email_submit": "更新邮件提醒设置"
            }
            yield scrapy.FormRequest(self.setting_url,formdata=fromdata,callback=self.parse_edit)

    def parse_edit(self,response):
        if "设置更新成功" in response.text:
            print("chenggong!")
        else:
            print("shibai!!!")



