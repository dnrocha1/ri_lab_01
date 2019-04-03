# -*- coding: utf-8 -*-
import scrapy
import json

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
        # print('*************************************************')
        # print(self.start_urls)
        # print('*************************************************')

    def parse(self, response):
        #
        # inclua seu código aqui
        #
        for href in response.css("div.td-block-span4 a::attr(href)"):
                yield response.follow(href, self.parse_post, meta={'url': response.url})
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        #
        #
        #
    def parse_post(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        print('\n')
        yield {
            'title': extract_with_css('h1.entry-title::text'),
            'author': extract_with_css('div.td-author-by + a::text'),
            'date': extract_with_css('time::text'),
            'url': response.url,
            'section': response.meta['url'].split('/')[-2],
            'text': response.xpath('//div[contains(@class, "td-post-content")]//p/text() | \
                                    //div[contains(@class, "td-post-content")]//p/span/text()').getall()#getall(default='').strip(),
            # response.xpath("//p/descendant::text()[not(parent::div/@class='td_block_template_1')]").getall()
        }
        print('\n')
