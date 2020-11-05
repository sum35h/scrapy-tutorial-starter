import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('hello this is my first spider')

        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield{
                'text': quote.css('.text::text').get(),
                'author':quote.css('.author::text').get(),
                'tags': quote.css('.tag::text').extract(),
            }
            
        author_url = quote.css('.author + a::attr(href)').get()
        self.logger.info('get author page url')
        # go to the author page
        yield response.follow(author_url, callback=self.parse_author)

        # next_page =  response.css('li.next a::attr(href)').get()  

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        for a in response.css('li.next a'):
                yield response.follow(a, callback=self.parse)


    def parse_author(self, response):
        yield {
            'author_name': response.css('.author-title::text').get(),
            'author_birthday': response.css('.author-born-date::text').get(),
            'author_bornlocation': response.css('.author-born-location::text').get(),
            'author_bio': response.css('.author-description::text').get(),
        }