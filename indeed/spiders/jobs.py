from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from indeed.items import IndeedItem
from scrapy.loader import ItemLoader


class IndeedSpider(CrawlSpider):
    name = "indeed"
    allowed_domains = ["www.indeed.com"]

    # manage date range
    # location (USA/Canada only),
    # and terms (full time only)

    def start_requests(self):
        args = dict(
            title=getattr(self, 'job', 'QA Automation Engineers OR SDET'),  # q
            location=getattr(self, 'loc', 'USA'),  # rbl
            jobtype=getattr(self, 'jobtype', 'fulltime'),  # jt
            age=getattr(self, 'age', None),  # fromage
        )

        url = "https://www.indeed.com/jobs?q={title}&rbl={location}&jt={jobtype}".format(
            **args)
        yield Request(url, self.parse)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.xpath('//div[contains(@class,"row")]')

        for site in sites:
            item = IndeedItem()

            company = site.xpath(
                ".//span[@class='company']//a/text()").extract_first()
            if not company:
                company = site.xpath(
                    ".//span[@class='company']/text()").extract_first()

            item['company'] = company.strip()

            # title
            title = site.xpath(
                './/a[@data-tn-element="jobTitle"]/@title[1]').extract_first()

            item['title'] = title

            # indeed url
            link = site.xpath(
                ".//span[@class='company']//a/@href").extract_first()
            if link:
                item['link'] = 'https://www.indeed.com' + link

            yield item
            # what to crawl next
            next_to_crawl = hxs.xpath(
                '//span[@class="pn"]/parent::a/@href').extract()
            for i in next_to_crawl:
                url = response.urljoin(i)
                yield Request(url)
