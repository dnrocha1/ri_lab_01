# -*- coding: utf-8 -*-
import scrapy
import json
import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class DiarioDoCentroDoMundoSpider(scrapy.Spider):
    name = 'diario_do_centro_do_mundo'
    allowed_domains = ['diariodocentrodomundo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
        with open('seeds/diario_do_centro_do_mundo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for href in response.css("div.td-block-span4 a::attr(href)"):
                yield response.follow(href, self.parse_post, meta={'url': response.url})
        
    def parse_post(self, response):

        def extract_generic(selector):
            return response.css(selector).get()

        def extract_text(selector):
            result = response.css(selector).getall()
            return ' '.join(result)
        
        def extract_section():
            return response.meta['url'].split('/')[-2]

        def extract_date(selector):
            date = extract_generic(selector)
            dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            return dt.strftime('%d/%m/%Y %H:%M:%S')

        yield {
            'title': extract_generic('h1.entry-title::text'),
            'sub_title': '',
            'author': extract_generic('div.td-author-by + a::text'),
            'date': extract_date('time::attr(datetime)'),
            'section': extract_section(),
            'text': extract_text('.p2::text, .s1::text, p:not(.donation_paragraph)::text'),
            'url': response.url
        }
