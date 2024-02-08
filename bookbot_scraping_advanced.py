import scrapy
from scrapy.crawler import CrawlerProcess
import time
from concurrent.futures import ThreadPoolExecutor

class AbeBooksSpider(scrapy.Spider):
    """
    Spider class to scrape data from AbeBooks website.
    """
    name = "abebooks"

    custom_settings = {
        'FEEDS': {'1000_all_providers_with_limit.csv': {'format': 'csv'}},  # Specify CSV output file
        'FEED_EXPORT_ENCODING': 'utf-8',  # Set encoding for CSV output
        'CONCURRENT_REQUESTS': 32,  # Increase the number of concurrent requests
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Limit concurrent requests per domain
    }

    def start_requests(self):
        """
        Method to start the scraping process by sending requests to each page of listings.
        """
        base_url = "https://www.abebooks.de/servlet/SearchResults?prevpage={}&bi=0&bsi={}&sortby=1&vci=87044093&ds=50"
        max_pages = 30

        # Generate requests for each page of listings
        for page_number in range(max_pages):
            url = base_url.format(page_number, page_number * 50)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Method to parse the listing items on each page.
        """
        listing_items = response.css('li[data-cy="listing-item"]')
        with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
            # Submit scraping tasks to the thread pool
            futures = [executor.submit(self.parse_listing, item, response) for item in listing_items]
            # Retrieve results from completed tasks
            for future in futures:
                future.result()

    def parse_listing(self, item, response):
        """
        Method to parse individual listing pages.
        """
        link = item.css('a[id*=listing]::attr(href)').get()
        full_link = response.urljoin(link)
        yield scrapy.Request(full_link, callback=self.parse_buying_options)

    def parse_buying_options(self, response):
        """
        Method to parse the buying options on listing pages.
        """
        listing_items = response.css('li[data-cy="listing-item"]')
        for item in listing_items:
            price = item.css('meta[itemprop="price"]::attr(content)').get()
            seller_link = item.css('a[data-cy="listing-seller-link"]::text').get()
            country_text = item.css('a[data-cy="listing-seller-link"]::text').get()
            country = country_text.split(',')[-1].strip() if country_text else None
            isbn = item.css('meta[itemprop="isbn"]::attr(content)').get()
            title = item.css('span[data-cy="listing-title"]::text').get()

            yield {
                'ISBN13': isbn,
                'Title': title,
                'Provider': seller_link,
                'Country': country,
                'Price': price
            }

def main():
    """
    Main function to run the Scrapy spider and display summary.
    """
    start_time = time.time()

    # Run the AbeBooksSpider spider
    process = CrawlerProcess()
    process.crawl(AbeBooksSpider)
    process.start()

    end_time = time.time()
    running_time = end_time - start_time
    print("Total running time:", running_time, "seconds")

if __name__ == "__main__":
    main()
