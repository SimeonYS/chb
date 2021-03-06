import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import ChbItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class ChbSpider(scrapy.Spider):
	name = 'chb'
	start_urls = ['https://www.chb.cw/eid/28166?p=1']

	def parse(self, response):
		post_links = response.xpath('//div[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="nextprev"]/a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//div[@class="date"]/text()').get()
		title = response.xpath('//div[@class="title"]/text()').get()
		content = response.xpath('//div[@class="newsItem"]//text()[not (ancestor::div[@class="title"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=ChbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
