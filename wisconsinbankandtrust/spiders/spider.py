import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import WisconsinbankandtrustItem
from itemloaders.processors import TakeFirst


class WisconsinbankandtrustSpider(scrapy.Spider):
	name = 'wisconsinbankandtrust'
	start_urls = ['https://www.wisconsinbankandtrust.com/customer-service/about/news']

	def parse(self, response):
		post_links = response.xpath('//a[@aria-described-by]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Go to next page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="region region-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		try:
			date = re.findall(r'[A-Za-z]+\s\d{1,2},\s\d{4}', description)[0]
		except:
			date = ''

		item = ItemLoader(item=WisconsinbankandtrustItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
